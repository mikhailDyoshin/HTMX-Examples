from .types import Page

PAGES = (
    Page("/", "Home", "partials/home.html"),
    Page("/settings", "Settings", "partials/settings.html"),
    Page("/users", "Users", "partials/users.html"),
)
