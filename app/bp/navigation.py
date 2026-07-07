from flask import Blueprint, render_template, request
from dataclasses import dataclass

from flask.typing import RouteCallable


bp = Blueprint("navigation", __name__, url_prefix="")


@dataclass(frozen=True)
class Page:
    url: str
    title: str
    template: str
    context: object = None


PAGES = (
    Page("/", "Home", "partials/home.html"),
    Page("/settings", "Settings", "partials/settings.html"),
)


def is_hx_request() -> bool:
    return bool(request.headers.get("HX-Request"))


def navigation_oob_template(active_page: Page) -> str:
    return render_template(
        "/partials/navigation_oob.html", pages=PAGES, active_page=active_page
    )


def render_page(page: Page) -> str:
    return render_template(
        "/page.html",
        content_template=page.template,
        content_data=page.context,
        pages=PAGES,
        active_page=page,
    )


def render_partial(page: Page) -> str:
    return render_template(page.template, data=page.context) + navigation_oob_template(
        page
    )


def render(page: Page) -> str:
    if is_hx_request():
        return render_partial(page)
    return render_page(page)


def page_view(page: Page) -> RouteCallable:
    def view():
        return render(page)

    return view


for p in PAGES:
    bp.add_url_rule(
        rule=p.url,
        endpoint=p.title.lower(),
        view_func=page_view(p),
    )
