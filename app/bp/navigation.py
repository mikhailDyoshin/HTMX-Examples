from typing import Any

from flask import Blueprint, Request, render_template, request
from dataclasses import dataclass
from app.utils import is_hx_request, name_to_path
from enum import Enum, StrEnum

bp = Blueprint("navigation", __name__, url_prefix="")


@dataclass(frozen=True)
class NavigationLink:
    url: str
    text: str
    style: str


@dataclass(frozen=True)
class Navigation:
    style: str
    items: tuple[NavigationLink, ...]


class NavigationUrl(StrEnum):
    HOME = "/"
    SETTINGS = "/settings"


@dataclass(frozen=True)
class NavigationRouteData:
    url: str
    link_text: str
    template_name: str


class NavigationRoute(Enum):
    HOME = NavigationRouteData(
        url=NavigationUrl.HOME, link_text="Home", template_name="home"
    )
    SETTINGS = NavigationRouteData(
        url=NavigationUrl.SETTINGS, link_text="Settings", template_name="settings"
    )


def nav_link(
    current_item: NavigationRoute, selected_item: NavigationRoute
) -> NavigationLink:
    style = "active" if selected_item is current_item else ""
    return NavigationLink(
        url=current_item.value.url,
        text=current_item.value.link_text,
        style=" ".join(("", style)),
    )


def navigation_links(active: NavigationRoute) -> tuple[NavigationLink, ...]:
    return tuple([nav_link(i, active) for i in NavigationRoute])


def navigation_data(active_menu_item: NavigationRoute) -> Navigation:
    return Navigation(
        items=navigation_links(active_menu_item),
        style="",
    )


def navigation_template(active_menu_item: NavigationRoute) -> str:
    return render_template(
        "/partials/navigation_oob.html",
        navigation_data=navigation_data(active_menu_item),
    )


def render_page(
    request: Request,
    active_menu_item: NavigationRoute,
    template_name: str,
    page_data: Any,
) -> str:
    if is_hx_request(request):
        return render_template(
            name_to_path(template_name), data=page_data
        ) + navigation_template(active_menu_item)
    return render_template(
        "/page.html",
        path_to_partial=name_to_path(template_name),
        page_data=page_data,
        navigation_data=navigation_data(active_menu_item),
    )


@bp.route(NavigationUrl.HOME)
def home():
    return render_page(request, NavigationRoute.HOME, "home", None)


@bp.route(NavigationUrl.SETTINGS)
def settings():
    return render_page(request, NavigationRoute.SETTINGS, "settings", None)
