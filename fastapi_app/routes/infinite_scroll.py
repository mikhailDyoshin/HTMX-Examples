from dataclasses import dataclass
from fastapi import APIRouter, Request, Query
from fastapi_app.templates import templates


router = APIRouter(prefix="/scroll")

data = [i for i in range(0, 200)]
PAGE_SIZE = 20


def listener(page: int) -> dict[str, str]:
    return {
        "hx-get": f"/scroll/get?page={page}",
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


def render_page(request: Request, page: int):
    return templates.TemplateResponse(
        "infinite_scroll/bulk.html", {"request": request, "items": create_page(page)}
    )


@router.get("/load")
async def load_list(request: Request):
    return render_page(request, 0)


@router.get("/get")
async def get_page(request: Request, page: int = Query(0)):
    next_page = page + 1
    return render_page(request, next_page)
