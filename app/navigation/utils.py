from flask import Blueprint, render_template, request
from .types import Page
from .pages import PAGES
from flask.typing import RouteCallable


def is_hx_request() -> bool:
    return bool(request.headers.get("HX-Request"))


def navigation_oob_template(active_page: Page) -> str:
    return render_template(
        "navigation/navigation_oob.html", pages=PAGES, active_page=active_page
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


def register_navigation_routes(navigation_blueprint: Blueprint):
    for p in PAGES:
        navigation_blueprint.add_url_rule(
            rule=p.url,
            endpoint=p.title.lower(),
            view_func=page_view(p),
        )
