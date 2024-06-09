# app/auth/__init__.py

from flask import Blueprint

auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/auth/static",
)


from . import routes
