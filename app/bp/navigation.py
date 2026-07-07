from typing import Any

from flask import Blueprint, Request, render_template, request
from dataclasses import dataclass
from enum import Enum

from flask.typing import RouteCallable


bp = Blueprint("navigation", __name__, url_prefix="")

PARTIALS_DIR = "/partials"
NAVIGATION_TEMPLATE = f"{PARTIALS_DIR}/side_bar.html"


@dataclass(frozen=True)
class NavigationLink:
    url: str
    text: str
    style: str


@dataclass(frozen=True)
class NavigationRoute:
    url: str
    link_text: str


@dataclass(frozen=True)
class Partial:
    template: str
    data: Any


@dataclass(frozen=True)
class Page:
    navigation: Partial
    content: Partial


def partial_template(name: str) -> str:
    return f"partials/{name}.html"


class Pages(Enum):
    HOME = Page(
        navigation=Partial(NAVIGATION_TEMPLATE, NavigationRoute("/", "Home")),
        content=Partial(partial_template("home"), None),
    )
    SETTINGS = Page(
        navigation=Partial(
            NAVIGATION_TEMPLATE,
            NavigationRoute("/settings", "Settings"),
        ),
        content=Partial(partial_template("settings"), None),
    )


NAVIGATION_ROUTES: tuple[NavigationRoute, ...] = tuple(
    [p.value.navigation.data for p in Pages]
)


def is_hx_request(request: Request) -> bool:
    return bool(request.headers.get("HX-Request"))


def nav_link(
    current_item: NavigationRoute, selected_item: NavigationRoute
) -> NavigationLink:
    style = "active" if selected_item is current_item else ""
    return NavigationLink(
        url=current_item.url,
        text=current_item.link_text,
        style=" ".join(("", style)).strip(),
    )


def navigation_links(active: NavigationRoute) -> tuple[NavigationLink, ...]:
    return tuple([nav_link(i, active) for i in NAVIGATION_ROUTES])


def navigation_oob_template(active_menu_item: NavigationRoute) -> str:
    return render_template(
        "/partials/navigation_oob.html",
        navigation_data=navigation_links(active_menu_item),
    )


def render_page(page: Pages) -> str:
    return render_template(
        "/page.html",
        content_template=page.value.content.template,
        content_data=page.value.content.data,
        navigation_data=navigation_links(page.value.navigation.data),
    )


def render_partial(page: Pages) -> str:
    return render_template(
        page.value.content.template, data=page.value.content.data
    ) + navigation_oob_template(page.value.navigation.data)


def render(request: Request, page: Pages) -> str:
    if is_hx_request(request):
        return render_partial(page)
    return render_page(page)


def page_view(page: Pages) -> RouteCallable:
    def view():
        return render(request, page)

    return view


for p in Pages:
    bp.add_url_rule(
        rule=p.value.navigation.data.url,
        endpoint=p.name.lower(),
        view_func=page_view(p),
    )
