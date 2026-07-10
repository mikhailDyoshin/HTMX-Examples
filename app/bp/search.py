from typing import List

from flask import Blueprint, render_template, request

from app.html_list import HtmlList, View


bp = Blueprint("search", __name__, url_prefix="/search")

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


@bp.post("/get")
def get_page():
    value = request.form.to_dict().get("search", "Nothing found")
    return render_template(
        "/macros/list.html", list=HtmlList("list", "list", search_result(value))
    )
