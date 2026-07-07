from flask import Blueprint, render_template, request
from .types import Page
from flask.typing import RouteCallable


def _is_hx_request() -> bool:
    return bool(request.headers.get("HX-Request"))


def _navigation_oob_template(active_page: Page, pages: tuple[Page, ...]) -> str:
    return render_template(
        "navigation/navigation_oob.html", pages=pages, active_page=active_page
    )


def _render_page(page: Page, pages: tuple[Page, ...]) -> str:
    return render_template(
        "/page.html",
        content_template=page.template,
        content_data=page.context,
        pages=pages,
        active_page=page,
    )


def _render_partial(page: Page, pages: tuple[Page, ...]) -> str:
    return render_template(page.template, data=page.context) + _navigation_oob_template(
        page, pages
    )


def _render(page: Page, pages: tuple[Page, ...]) -> str:
    if _is_hx_request():
        return _render_partial(page, pages)
    return _render_page(page, pages)


def _page_view(page: Page, pages: tuple[Page, ...]) -> RouteCallable:
    def view():
        return _render(page, pages)

    return view


def register_pages(navigation_blueprint: Blueprint, pages: tuple[Page, ...]):
    for p in pages:
        navigation_blueprint.add_url_rule(
            rule=p.url,
            endpoint=p.title.lower(),
            view_func=_page_view(p, pages),
        )
