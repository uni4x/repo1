# app/main/routes/customer_info.py

from flask import Blueprint, flash, redirect, render_template, session, url_for

from ..forms import CustomerInfoForm

bp = Blueprint("customer_info", __name__, url_prefix="/customer_info")


@bp.route("/<int:room_id>", methods=["GET", "POST"])
def customer_info(room_id):
    form = CustomerInfoForm()
    reservation_info = session.get("reservation_info", {})
    checkin_date = reservation_info.get("checkin_date")
    checkout_date = reservation_info.get("checkout_date")

    if form.validate_on_submit():
        # 顧客情報をセッションに保存
        session["customer_info"] = {
            "name": form.name.data,
            "address": form.address.data,
            "phone": form.phone.data,
            "email": form.email.data,
            "note": form.note.data,
            "number_of_guests": form.number_of_guests.data,
            "payment_type": form.payment_type.data,
        }
        flash("Customer information submitted successfully!", "success")
        return redirect(url_for("main.confirmation.confirmation", room_id=room_id))
    else:
        # デバッグ用メッセージ
        print("Form validation failed")
        print(form.errors)

    return render_template(
        "customer_info.html",
        form=form,
        room_id=room_id,
        checkin_date=checkin_date,
        checkout_date=checkout_date,
    )
