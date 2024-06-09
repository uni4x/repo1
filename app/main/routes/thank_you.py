# app/main/routes/thank_you.py

from flask import Blueprint, render_template, session

from ...models import Customer, Room

bp = Blueprint("thank_you", __name__)


@bp.route("/thank_you/<int:room_id>/<int:customer_id>", methods=["GET"])
def thank_you(room_id, customer_id):
    room = Room.query.get_or_404(room_id)
    customer = Customer.query.get_or_404(customer_id)
    reservation_info = session.get("reservation_info")
    customer_info = session.get("customer_info")
    number_of_guests = customer_info["number_of_guests"]
    if reservation_info:
        checkin_date = reservation_info["checkin_date"]
        checkout_date = reservation_info["checkout_date"]
    else:
        checkin_date = None
        checkout_date = None

    # セッションから顧客情報を削除
    session.pop("customer_info", None)
    session.pop("reservation_info", None)

    return render_template(
        "thank_you.html",
        room=room,
        customer=customer,
        checkin_date=checkin_date,
        checkout_date=checkout_date,
        number_of_guests=number_of_guests,
    )
