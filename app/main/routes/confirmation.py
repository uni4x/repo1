# app/main/routes/confirmation.py

from flask import Blueprint, render_template, redirect, url_for, session, flash
from ...models import Room, Reservation, Customer
from app import db
from datetime import datetime
from ..forms import ConfirmationForm

bp = Blueprint("confirmation", __name__, url_prefix="/confirmation")


@bp.route("/<int:room_id>", methods=["GET", "POST"])
def confirmation(room_id):
    room = Room.query.get_or_404(room_id)
    reservation_info = session.get("reservation_info")
    customer_info = session.get("customer_info")

    # デバッグ: セッションデータの確認
    print(f"reservation_info: {reservation_info}")
    print(f"customer_info: {customer_info}")

    if reservation_info and customer_info:
        checkin_date = reservation_info["checkin_date"]
        checkout_date = reservation_info["checkout_date"]
        number_of_guests = customer_info["number_of_guests"]
        payment_type = customer_info["payment_type"]
    else:
        flash("No reservation or customer information found in session.", "error")
        # return redirect(url_for('main.search.search'))
        return redirect(url_for("main.customer_info.customer_info", room_id=room_id))

    form = ConfirmationForm()

    if form.validate_on_submit():
        # 顧客情報をデータベースに保存
        customer = Customer(
            name=customer_info["name"],
            address=customer_info["address"],
            phone=customer_info["phone"],
            email=customer_info["email"],
            note=customer_info["note"],
        )
        db.session.add(customer)
        db.session.commit()

        # 予約をデータベースに保存
        reservation = Reservation(
            checkin_date=datetime.strptime(checkin_date, "%Y-%m-%d"),
            checkout_date=datetime.strptime(checkout_date, "%Y-%m-%d"),
            customer_id=customer.id,
            room_id=room_id,
            payment_type=payment_type,
            payment_status="unpaid",
            number_of_guests=number_of_guests,
        )
        db.session.add(reservation)
        db.session.commit()

        flash("Reservation confirmed!", "success")
        return redirect(
            url_for(
                "main.thank_you.thank_you", room_id=room_id, customer_id=customer.id
            )
        )

    return render_template(
        "confirmation.html",
        room=room,
        customer_info=customer_info,
        checkin_date=checkin_date,
        checkout_date=checkout_date,
        payment_type=payment_type,
        form=form,
        room_id=room_id,
        number_of_guests=number_of_guests,
    )
