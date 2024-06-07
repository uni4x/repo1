# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from app import db
from app.models import RoomType, Employee
from app.roomtype.forms import RoomTypeForm
from app.employee.forms import EmployeeForm

admin = Blueprint('admin', __name__)

@admin.route('/admin_dashboard')
@login_required
def admin_dashboard():
    user_role = session.get('role', 'employee')

    # 管理者のみ全項目を表示
    if current_user.is_admin:
        room_types = RoomType.query.all()
        employees = Employee.query.filter(Employee.deleted_at.is_(None)).all()
        return render_template('admin_dashboard.html', room_types=room_types, employees=employees, role=user_role)
    else:
        # 一般従業員は従業員用画面の表示
        room_types = RoomType.query.all()
        return render_template('admin_dashboard.html', room_types=room_types, role=user_role)

# # 管理者のみ全項目を表示
#     if current_user.is_admin:
#         room_types = RoomType.query.all()
#         employees = Employee.query.filter(Employee.deleted_at.is_(None)).all()
#         return render_template('admin_dashboard.html', room_types=room_types, employees=employees, role=user_role)
#     else:
#         # 一般従業員は従業員管理のみ表示
#         employees = Employee.query.filter(Employee.deleted_at.is_(None)).all()
#         return render_template('admin_dashboard.html', employees=employees, role=user_role)