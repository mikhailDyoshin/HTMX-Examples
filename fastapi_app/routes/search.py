from typing import List


from fastapi import Request, APIRouter
from starlette.responses import HTMLResponse
from app.html_list import HtmlList, View
from fastapi_app.templates import templates

router = APIRouter(prefix="/search")

DATA = (
    "Albert Einstein",
    "Marie Curie",
    "Leonardo da Vinci",
    "Isaac Newton",
    "Mahatma Gandhi",
    "Martin Luther King Jr.",
    "Aristotle",
    "Ada Lovelace",
)


def search_result(substing: str) -> List[View[str]]:
    return [
        View(s, "/search/list_item.html")
        for s in DATA
        if (substing.lower() in s.lower())
    ]


@router.post("/get", response_class=HTMLResponse)
async def get_page(request: Request):
    form_data = await request.form()

    value = form_data.get("search", "Nothing found")

    list_data = HtmlList(id="list", style="list", items=search_result(value))

    return templates.TemplateResponse(
        "macros/list.html", {"request": request, "list": list_data}
    )
