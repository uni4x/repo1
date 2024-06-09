# app/main/routes/reserve.py

from flask import Blueprint, redirect, render_template, request, session, url_for

from app import db

from ...models import Room
from ..forms import ReservationForm

bp = Blueprint("reserve", __name__)


@bp.route("/reserve/<int:room_id>", methods=["GET", "POST"])
def reserve(room_id):
    room = Room.query.get_or_404(room_id)
    form = ReservationForm()

    # セッションからチェックインとチェックアウトの日付を取得
    reservation_info = session.get("reservation_info", {})
    checkin_date = reservation_info.get(
        "checkin_date", request.args.get("checkin_date")
    )
    checkout_date = reservation_info.get(
        "checkout_date", request.args.get("checkout_date")
    )

    if form.validate_on_submit():
        # 予約情報をセッションに保存
        session["reservation_info"] = {
            "room_id": room_id,
            "checkin_date": checkin_date,
            "checkout_date": checkout_date,
        }
        return redirect(url_for("main.customer_info.customer_info", room_id=room_id))

    return render_template(
        "reservation_top.html",
        form=form,
        room=room,
        checkin_date=checkin_date,
        checkout_date=checkout_date,
    )
