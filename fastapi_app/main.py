import asyncio
import json
from datetime import datetime
from fastapi import APIRouter, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from flask import request
from sse_starlette import EventSourceResponse
from pathlib import Path
from app.navigation.types import Page
from fastapi_app.sensor import Sensor, get_sensor_reading, recent_readings
from .navigation.utils import register_pages

app = FastAPI()
router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

sensor = Sensor()

PAGES = (
    Page("/", "Home", "/partials/home.html"),
    Page("/dashboard", "Dashboard", "dashboard/dashboard.html"),
)
register_pages(router, PAGES, templates)

app.include_router(router=router)


# # Hot reload magic for development (because restarting servers is for losers)
# if os.getenv("DEBUG"):
#     hot_reload = arel.HotReload(paths=["."])
#     app.add_websocket_route("/hot-reload", route=hot_reload)
#     app.add_event_handler("startup", hot_reload.startup)
#     app.add_event_handler("shutdown", hot_reload.shutdown)
#     templates.env.globals["DEBUG"] = True
#     templates.env.globals["hot_reload"] = hot_reload
#


@app.get("/stream")
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

                # Send to all connected browsers
                yield {"event": "sensor_update", "data": clean_html}

                await asyncio.sleep(2)  # Update every 2 seconds
        except asyncio.CancelledError:
            # User closed browser/tab - no drama, just stop
            pass

    return EventSourceResponse(event_generator())


@app.get("/chart-data")
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


@app.get("/health")
async def health_check():
    """Because production servers need to know we're alive"""
    return {"status": "alive_and_kicking", "timestamp": datetime.now().isoformat()}
