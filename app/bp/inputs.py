from flask import Blueprint, render_template

from app.html_input import HtmlInput, input_write
from app.html_list import HtmlList


bp = Blueprint("inputs", __name__, url_prefix="/inputs")


inputs_data = [
    HtmlInput(label="Text", style="text-input", value="Hello", attrs={"type": "text"}),
    HtmlInput(label="Text", style="text-input", value="World"),
]

inputs: HtmlList[HtmlInput] = HtmlList(
    "list", "list", [input_write(i) for i in inputs_data]
)


@bp.get("/")
def get_inputs():
    print("Inputs")
    return render_template(
        "/macros/list.html",
        list=inputs,
    )
