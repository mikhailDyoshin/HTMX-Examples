from dataclasses import dataclass, field
from flask import Blueprint, render_template
import threading
import time

bp = Blueprint("progress_bar", __name__, url_prefix="/progress_bar")


@dataclass
class Progress:
    value: int = 0
    maximum: int = 100
    step: int = 10
    delay: float = 0.5

    _thread: threading.Thread | None = field(default=None, init=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    @property
    def finished(self):
        with self._lock:
            return self.value >= self.maximum

    def _run(self):
        while True:
            with self._lock:
                if self.value >= self.maximum:
                    break
                self.value += self.step

            time.sleep(self.delay)

    def start(self):
        with self._lock:
            self.value = 0

        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def get_value(self):
        with self._lock:
            return self.value


progress = Progress()


@dataclass(frozen=True)
class ProgressBar:
    value: int
    value_min: int = 0
    value_max: int = 100


def _render_progress_bar(value: int) -> str:
    return render_template("/progress_bar/progress_bar.html", data=ProgressBar(value))


progress = Progress()


@bp.post("/start")
async def start():
    progress.start()
    return render_template("/progress_bar/trigger.html")


@bp.get("/progress")
def get_progress():
    if progress.finished:
        return _render_progress_bar(progress.get_value()), 200, {"HX-Trigger": "done"}
    return _render_progress_bar(progress.get_value())


@bp.get("/end")
def end():
    return "Finished"
