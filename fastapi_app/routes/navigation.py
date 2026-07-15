from collections.abc import Callable

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.navigation.types import Page
from fastapi_app.templates import templates


router = APIRouter()

PAGES = (
    Page(url="/", title="Home", route_name="home", template="/partials/home.html"),
    Page(
        url="/dashboard",
        title="Dashboard",
        route_name="dashboard",
        template="dashboard/dashboard.html",
    ),
    Page(
        url="/search",
        title="Search",
        route_name="search",
        template="search/search.html",
    ),
    Page(
        url="/infinite_scroll",
        title="Infinite Scroll",
        route_name="infinite_scroll",
        template="infinite_scroll/list.html",
    ),
)


def _is_hx_request(request: Request) -> bool:
    return request.headers.get("HX-Request") is not None


def _navigation_oob_template(
    request: Request,
    page: Page,
    pages: tuple[Page, ...],
    templates: Jinja2Templates,
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


def _register_pages(
    pages: tuple[Page, ...],
    templates,
) -> None:
    for page in pages:
        router.add_api_route(
            page.url,
            _page_view(page, pages, templates),
            methods=["GET"],
            name=page.route_name.lower(),
            response_class=HTMLResponse,
        )


_register_pages(PAGES, templates)
