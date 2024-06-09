# app/room/__init__.py

from flask import Blueprint

room = Blueprint(
    "room",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/room/static",
)

from . import routes
