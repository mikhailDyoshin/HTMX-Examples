import asyncio
import json
from datetime import datetime
from fastapi import Request, APIRouter
from flask import request
from sse_starlette import EventSourceResponse
from app.view import View
from fastapi_app.sensor import Sensor, get_sensor_reading, recent_readings
from fastapi_app.status import Status
from fastapi_app.templates import templates
from fastapi_app.routes.utils import render_toast

router = APIRouter()
sensor = Sensor()


@router.get("/stream")
async def stream_sensor_data():
    """The magic streaming endpoint that makes everything work"""

    async def event_generator():
        try:
            while True:
                # Generate new sensor reading
                data = sensor.generate_reading()
                recent_readings.append(data)  # Store for charts
                context = {"request": request, "data": get_sensor_reading(data)}
                template = templates.get_template(
                    "/dashboard/sensor_readings.html"
                ).render(context)
                clean_html = "".join(template.splitlines())

                if data.status is Status.CRITICAL:
                    message = {
                        "request": request,
                        "message": View(data, "/dashboard/critical_alert.html"),
                    }
                    clean_toast = "".join(render_toast(message, templates).splitlines())
                    clean_html += clean_toast

                # Send to all connected browsers
                yield {"event": "sensor_update", "data": clean_html}

                await asyncio.sleep(2)  # Update every 2 seconds
        except asyncio.CancelledError:
            # User closed browser/tab - no drama, just stop
            pass

    return EventSourceResponse(event_generator())


@router.get("/chart-data")
async def get_chart_data(request: Request):
    """Prepare data for Chart.js visualization"""
    # Ensure we have enough data for charts
    if len(recent_readings) < 20:
        for _ in range(20):
            recent_readings.append(sensor.generate_reading())

    temp_data = [r.temperature for r in recent_readings]
    humidity_data = [r.humidity for r in recent_readings]
    labels = [str(i) for i in range(len(recent_readings))]

    return templates.TemplateResponse(
        "/dashboard/chart_data.html",
        {
            "request": request,
            "temp_data": json.dumps(temp_data),
            "humidity_data": json.dumps(humidity_data),
            "labels": json.dumps(labels),
        },
    )


@router.get("/health")
async def health_check():
    """Because production servers need to know we're alive"""
    return {"status": "alive_and_kicking", "timestamp": datetime.now().isoformat()}
