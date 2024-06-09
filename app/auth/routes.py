# app/auth/routes.py

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import UserMixin, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from ..models import Employee
from . import auth
from .forms import LoginForm


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Employee.query.filter_by(name=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            # ユーザーの役割をセッションに追加
            session["role"] = "admin" if user.is_admin else "employee"
            return redirect(url_for("admin.admin_dashboard"))  # ブループリント名を追加
        flash("ユーザー名またはパスワードが違います", "error")
    return render_template("login.html", form=form)


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    # ログアウト時にセッションから役割を削除
    session.pop("role", None)
    logout_user()
    return redirect(url_for("auth.login"))
