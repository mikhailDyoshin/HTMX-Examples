from fastapi.templating import Jinja2Templates


def render_toast(context: dict, templates: Jinja2Templates) -> str:
    return templates.get_template("/partials/toast_message.html").render(context)
