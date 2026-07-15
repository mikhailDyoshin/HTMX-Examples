from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_app.routes import dashboard, toast, navigation, search, infinite_scroll
from fastapi_app.templates import BASE_DIR

app = FastAPI()
router = APIRouter()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


app.include_router(router=navigation.router)
app.include_router(router=dashboard.router)
app.include_router(router=toast.router)
app.include_router(router=search.router)
app.include_router(router=infinite_scroll.router)
