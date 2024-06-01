# app/employee/__init__.py

from flask import Blueprint

employee = Blueprint('employee', __name__, template_folder='templates', static_folder='static', static_url_path='/employee/static')


from . import routes
