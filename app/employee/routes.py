# app/employee/routes.py

from flask import render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_required, current_user
from .forms import RegisterForm, EmployeeForm
from ..models import Employee
from app import db
from . import employee
from werkzeug.security import generate_password_hash
from datetime import datetime
from app.decorators import admin_required


# 既存の従業員管理ルート
@employee.route("/employees", defaults={"id": None}, methods=["GET", "POST"])
@employee.route("/employees/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def employees(id):
    if not current_user.is_admin:
        flash("管理者のみアクセス可能です。")
        return redirect(url_for("auth.login"))

    # 新規登録、一覧、編集
    # idがある場合は編集、ない場合は新規登録
    if id:
        employee = Employee.query.get_or_404(id)
        form = EmployeeForm(request.form, obj=employee)
    else:
        employee = Employee()
        form = EmployeeForm(request.form)

    # JSONデータを要求する場合
    if request.args.get("mode") == "json":
        employee = Employee.query.get_or_404(id)
        return jsonify(
            {
                "id": employee.id,
                "name": employee.name,
                "description": employee.description,
            }
        )

    # POSTでデータが送信された場合
    if request.method == "POST":
        if form.validate():
            if id:
                employee.name = request.form.get("name2", employee.name)
                employee.description = request.form.get(
                    "description2", employee.description
                )
                password = request.form.get("password2")
                if password:
                    employee.password = password
            else:
                form.populate_obj(employee)
                password = request.form.get("password")
                if password:
                    employee.password = password
                db.session.add(employee)
            db.session.commit()
            flash("変更が保存されました。", "success")
            return redirect(url_for("employee.employees"))
        else:
            flash("入力値に問題があります。", "error")

    # idがあればそのデータをフォームにロード
    if id:
        employee = Employee.query.get_or_404(id)
        form = EmployeeForm(obj=employee)

    # 既存の検索クエリの初期設定
    # query = Employee.query
    query = Employee.query.filter(Employee.deleted_at.is_(None))

    # nameに基づくフィルタリング条件の適用
    search_name = request.args.get("search_name")
    if search_name:
        query = query.filter(Employee.name.contains(search_name))

    # descriptionに基づくフィルタリング条件の適用
    search_description = request.args.get("search_description")
    if search_description:
        query = query.filter(Employee.description.contains(search_description))

    # ソートオーダーの取得と適用
    sort_order = request.args.get("sort_order", "asc")
    if sort_order == "asc":
        query = query.order_by(Employee.name.asc())
    else:
        query = query.order_by(Employee.name.desc())

    # ページネーションの設定
    page = request.args.get("page", 1, type=int)
    per_page = 5
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    employees = pagination.items

    return render_template(
        "employees.html",
        employees=employees,
        pagination=pagination,
        sort_order=sort_order,
        form=form,
        id=id,
    )


# 削除用のルート（論理削除）
@employee.route("/employee/<int:id>", methods=["POST"])
@login_required
def delete_employee(id):
    if not current_user.is_admin:
        flash("管理者のみアクセス可能です。")
        return redirect(url_for("auth.login"))

    try:
        employee = Employee.query.get_or_404(id)
        employee.deleted_at = datetime.utcnow()  # 削除日を設定
        db.session.commit()
        flash("削除しました", "success")
    except Exception as e:
        db.session.rollback()
        flash(str(e), "error")
    return redirect(url_for("employee.employees"))
