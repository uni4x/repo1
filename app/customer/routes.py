# app/customer/routes.py

from datetime import datetime

from flask import flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

from app import db

from ..models import Customer
from . import customer
from .forms import CustomerForm


@customer.route("/customers", defaults={"id": None}, methods=["GET", "POST"])
@customer.route("/customers/<int:id>", methods=["GET", "POST"])
@login_required
def customers(id):
    if id:
        customer = Customer.query.get_or_404(id)
        form = CustomerForm(request.form, obj=customer)
    else:
        customer = Customer()
        form = CustomerForm(request.form)

    if request.args.get("mode") == "json":
        customer = Customer.query.get_or_404(id)
        return jsonify(
            {
                "id": customer.id,
                "name": customer.name,
                "address": customer.address,
                "phone": customer.phone,
                "email": customer.email,
                "note": customer.note,
            }
        )

    if request.method == "POST":
        if form.validate():
            form.populate_obj(customer)
            try:
                if not id:
                    db.session.add(customer)
                db.session.commit()
                flash("Customer information saved successfully!", "success")
            except IntegrityError as e:
                db.session.rollback()
                error_message = "データベースエラー: "
                if "UNIQUE constraint failed" in str(e.orig):
                    error_message += "入力された情報は既に存在します。"
                else:
                    error_message += "不明なエラーが発生しました。"
                flash(error_message, "error")
            except Exception as e:
                db.session.rollback()
                flash(f"予期しないエラーが発生しました: {str(e)}", "error")
            return redirect(url_for("customer.customers"))
        else:
            flash("Please correct the errors in the form.", "error")

    query = Customer.query.filter(
        Customer.deleted_at.is_(None)
    )  # 論理削除されていない顧客のみを取得

    search_name = request.args.get("search_name")
    if search_name:
        query = query.filter(Customer.name.contains(search_name))

    sort_order = request.args.get("sort_order", "asc")
    if sort_order == "asc":
        query = query.order_by(Customer.name.asc())
    else:
        query = query.order_by(Customer.name.desc())

    page = request.args.get("page", 1, type=int)
    per_page = 5
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    customers = pagination.items

    return render_template(
        "customer.html",
        customers=customers,
        pagination=pagination,
        sort_order=sort_order,
        form=form,
        id=id,
    )


@customer.route("/customer/<int:id>", methods=["POST"])
def delete_customer(id):
    try:
        customer = Customer.query.get_or_404(id)
        customer.deleted_at = datetime.utcnow()  # 論理削除のために現在の日時を設定
        db.session.commit()
        flash("Customer deleted successfully", "success")
    except Exception as e:
        db.session.rollback()
        flash(str(e), "error")
    return redirect(url_for("customer.customers"))
