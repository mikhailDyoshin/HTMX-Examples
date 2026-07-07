from flask import Blueprint

from app.navigation.types import Page
from app.navigation.utils import register_pages


bp = Blueprint("navigation", __name__, url_prefix="")


PAGES = (
    Page("/", "Home", "partials/home.html"),
    Page("/settings", "Settings", "partials/settings.html"),
    Page("/users", "Users", "partials/users.html"),
)
register_pages(bp, PAGES)
