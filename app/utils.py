from flask import Request


def is_hx_request(request: Request) -> bool:
    return bool(request.headers.get("HX-Request"))


def name_to_path(name: str) -> str:
    return f"partials/{name}.html"
