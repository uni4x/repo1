
# app/main/routes/error_handlers.py

from flask import Blueprint, render_template
from flask_wtf.csrf import CSRFError

bp = Blueprint('error_handlers', __name__)

@bp.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400