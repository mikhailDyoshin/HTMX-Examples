from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.html_list import HtmlList, View
from fastapi_app.templates import templates
from typing import List

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


def search_result(substring: str) -> List[View[str]]:
    return [
        View(s, "/search/list_item.html")
        for s in DATA
        if (substring.lower() in s.lower())
    ]


@router.post("/get", response_class=HTMLResponse)
async def get_page(request: Request):
    # 1. Await the form extraction (returns a FormData object)
    form_data = await request.form()

    # 2. Extract the field with a default fallback
    value = form_data.get("search", "Nothing found")

    # 3. Create your data object
    list_data = HtmlList(id="list", style="list", items=search_result(value))

    # 4. Render template, explicitly passing the request object
    return templates.TemplateResponse(
        "macros/list.html", {"request": request, "list": list_data}
    )
