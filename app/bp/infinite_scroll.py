from dataclasses import dataclass

from flask import Blueprint, render_template, request


bp = Blueprint("infinite_scroll", __name__, url_prefix="/scroll")

data = [i for i in range(0, 50)]
PAGE_SIZE = 20


def listener(page: int) -> dict[str, str]:
    return {
        "hx-get": f"scroll/get/?page={page}",
        "hx-trigger": "intersect once",
        "hx-swap": "afterend",
    }


def get_data_by_page(page: int) -> list[int]:
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    return data[start:end]


@dataclass(frozen=True)
class Item:
    content: str
    attrs: dict[str, str] | None = None


def create_page(page: int) -> list[Item]:

    current_list = get_data_by_page(page)

    def is_last(i: int) -> bool:
        return i == len(current_list) - 1

    return [
        Item(
            content=str(data),
            attrs=listener(page) if is_last(i) else None,
        )
        for i, data in enumerate(current_list)
    ]


def render_page(page: int) -> str:
    items = create_page(page)
    return render_template("infinite_scroll/bulk.html", items=items)


@bp.get("/load")
def load_list():
    return render_page(0)


@bp.route("/get/")
def get_page():
    current_page = int(request.args.get("page", 0))
    next_page = current_page + 1
    return render_page(next_page)
