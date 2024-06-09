# app/reservation/__init__.py

from flask import Blueprint

# Blueprintを定義
reservation = Blueprint(
    "reservation",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/reservation/static",
)

from . import routes
