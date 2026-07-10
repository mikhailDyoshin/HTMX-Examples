from dataclasses import dataclass
from enum import StrEnum
from app.view import View


class InputMode(StrEnum):
    WRITE = "write"
    READ = "read"


@dataclass(frozen=True)
class HtmlInput:
    label: str
    style: str
    value: str
    attrs: dict[str, str] | None = None


def _render_input(mode: str, input: HtmlInput) -> View:
    return View(input, f"/macros/input_{mode}.html")


def input_write(input: HtmlInput) -> View:
    return _render_input("write", input)


def input_read(input: HtmlInput) -> View:
    return _render_input("read", input)
