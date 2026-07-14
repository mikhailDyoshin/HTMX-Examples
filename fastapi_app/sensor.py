from collections import deque
from dataclasses import dataclass
import random
from datetime import datetime

from fastapi_app.status import Status, get_status, get_style


@dataclass(frozen=True)
class SensorData:
    time: datetime
    temperature: float
    humidity: float
    status: Status


@dataclass(frozen=True)
class SensorReading:
    time: str
    temperature: str
    humidity: str
    status: str
    status_style: str


def get_sensor_reading(data: SensorData) -> SensorReading:

    return SensorReading(
        time=data.time.strftime("%H:%M:%S"),
        temperature=str(data.temperature),
        humidity=str(data.humidity),
        status=data.status.upper(),
        status_style=get_style(data.status),
    )


class Sensor:
    def __init__(self):
        # Room temperature range (adjust if you live in Antarctica)
        self.min_temp = 18.0
        self.max_temp = 26.0
        self.min_humidity = 30.0
        self.max_humidity = 65.0

    def generate_reading(self):
        return SensorData(
            time=datetime.now(),
            temperature=round(random.uniform(self.min_temp, self.max_temp), 1),
            humidity=round(random.uniform(self.min_humidity, self.max_humidity), 1),
            status=get_status(),
        )


# Store the last 20 readings (because nobody cares about data from 1995)
recent_readings: deque[SensorData] = deque(maxlen=20)
