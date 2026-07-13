from collections.abc import Callable

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.navigation.types import Page


def _is_hx_request(request: Request) -> bool:
    return request.headers.get("HX-Request") is not None


def _navigation_oob_template(
    request: Request,
    page: Page,
    pages: tuple[Page, ...],
    templates,
) -> str:
    return templates.get_template("navigation/navigation_oob.html").render(
        request=request,
        pages=pages,
        active_page=page,
    )


def _render_page(
    request: Request,
    page: Page,
    pages: tuple[Page, ...],
    templates,
) -> str:
    return templates.get_template("page.html").render(
        request=request,
        content_template=page.template,
        content_data=page.context,
        pages=pages,
        active_page=page,
    )


def _render_partial(
    request: Request,
    page: Page,
    pages: tuple[Page, ...],
    templates,
) -> str:
    return templates.get_template(page.template).render(
        request=request,
        data=page.context,
    ) + _navigation_oob_template(request, page, pages, templates)


def _render(
    request: Request,
    page: Page,
    pages: tuple[Page, ...],
    templates,
) -> str:
    if _is_hx_request(request):
        return _render_partial(request, page, pages, templates)
    return _render_page(request, page, pages, templates)


def _page_view(
    page: Page,
    pages: tuple[Page, ...],
    templates,
) -> Callable[[Request], HTMLResponse]:
    async def view(request: Request) -> HTMLResponse:
        return HTMLResponse(_render(request, page, pages, templates))

    return view


def register_pages(
    router: APIRouter,
    pages: tuple[Page, ...],
    templates,
) -> None:
    for page in pages:
        router.add_api_route(
            page.url,
            _page_view(page, pages, templates),
            methods=["GET"],
            name=page.title.lower(),
            response_class=HTMLResponse,
        )
