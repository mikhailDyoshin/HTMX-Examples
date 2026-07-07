from flask import Blueprint


from app.navigation.utils import register_navigation_routes


bp = Blueprint("navigation", __name__, url_prefix="")

register_navigation_routes(bp)
