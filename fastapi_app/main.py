from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()
router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


from app.navigation.types import Page
from .navigation.utils import register_pages


PAGES = (
    Page("/", "Home", "/partials/home.html"),
    Page("/dashboard", "Dashboard", "partials/dashboard.html"),
)
register_pages(router, PAGES, templates)

app.include_router(router=router)
