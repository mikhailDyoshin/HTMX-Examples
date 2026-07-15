from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi_app.templates import templates

router = APIRouter()


@router.get("/remove_message", response_class=HTMLResponse)
async def remove_message():
    return templates.get_template("/partials/toast.html").render()
