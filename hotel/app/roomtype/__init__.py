# app/roomtype/__init__.py

from flask import Blueprint

roomtype = Blueprint('roomtype', __name__, template_folder='templates', static_folder='static', static_url_path='/roomtype/static')


from . import routes
