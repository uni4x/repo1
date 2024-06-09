# app/routes.py

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from app import db
from app.employee.forms import EmployeeForm
from app.models import Employee, RoomType
from app.roomtype.forms import RoomTypeForm

admin = Blueprint("admin", __name__)


@admin.route("/admin_dashboard")
@login_required
def admin_dashboard():
    user_role = session.get("role", "employee")
    room_types = RoomType.query.all()
    employees = []

    # 管理者のみEmployeeテーブルを取得
    if current_user.is_admin:
        employees = Employee.query.filter(Employee.deleted_at.is_(None)).all()

    return render_template(
        "admin_dashboard.html",
        room_types=room_types,
        employees=employees,
        role=user_role,
    )
