# app/decorators.py

from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("ログインが必要です", "error")
            return redirect(url_for("auth.login"))
        if not current_user.is_admin:
            flash("管理者権限が必要です", "error")
            return redirect(url_for("admin.admin_dashboard"))
        return f(*args, **kwargs)

    return decorated_function
