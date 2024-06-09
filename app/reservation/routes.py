# app/reservation/routes.py

from flask import render_template, request, redirect, url_for, jsonify, flash, session
from flask_login import login_required, current_user
from . import reservation
from .forms import ReservationForm
from app import db
from ..models import Reservation, Customer, Room
from datetime import datetime


@reservation.route("/reservations", defaults={"id": None}, methods=["GET", "POST"])
@reservation.route("/reservations/<int:id>", methods=["GET", "POST"])
@login_required
def reservations(id):
    if id:
        reservation = Reservation.query.get_or_404(id)
        form = ReservationForm(request.form, obj=reservation)
    else:
        reservation = Reservation()
        form = ReservationForm(request.form)

    # モードが JSON の場合、予約データを返す
    if request.args.get("mode") == "json":
        reservation = Reservation.query.get_or_404(id)
        return jsonify(
            {
                "id": reservation.id,
                "checkin_date": reservation.checkin_date,
                "checkout_date": reservation.checkout_date,
                "customer_id": reservation.customer_id,
                "room_id": reservation.room_id,
                "payment_type": reservation.payment_type,
                "payment_status": reservation.payment_status,
                "number_of_guests": reservation.number_of_guests,
                "status": reservation.status,
            }
        )

    # POST リクエストの処理
    if request.method == "POST":
        checkin_date = form.checkin_date.data
        checkout_date = form.checkout_date.data
        form.update_room_choices(checkin_date, checkout_date)

        if form.validate():
            form.populate_obj(reservation)
            if not id:
                db.session.add(reservation)
            db.session.commit()
            return redirect(url_for("reservation.reservations"))
        else:
            flash("入力値に問題があります。", "error")

    # GET リクエストの処理
    query = Reservation.query.filter(
        Reservation.deleted_at.is_(None)
    )  # 論理削除されていない予約のみを取得

    search_customer = request.args.get("search_customer")
    if search_customer:
        query = query.join(Customer).filter(Customer.name.contains(search_customer))

    search_room = request.args.get("search_room")
    if search_room:
        query = query.join(Room).filter(Room.room_number.contains(search_room))

    sort_order = request.args.get("sort_order", "asc")
    if sort_order == "asc":
        query = query.order_by(Reservation.checkin_date.asc())
    else:
        query = query.order_by(Reservation.checkin_date.desc())

    page = request.args.get("page", 1, type=int)
    per_page = 5
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    reservations = pagination.items

    # フォームの初期化時にチェックイン日とチェックアウト日を渡す
    checkin_date = form.checkin_date.data or datetime.today().date()
    checkout_date = form.checkout_date.data or datetime.today().date()
    # update_room_choices メソッドを呼び出し、チェックイン日とチェックアウト日を元にフォームの選択肢を更新
    form.update_room_choices(checkin_date, checkout_date)

    return render_template(
        "reservation.html",
        reservations=reservations,
        pagination=pagination,
        sort_order=sort_order,
        form=form,
        id=id,
    )


@reservation.route("/reservation/<int:id>", methods=["POST"])
def delete_reservation(id):
    try:
        reservation = Reservation.query.get_or_404(id)
        reservation.deleted_at = datetime.utcnow()  # 論理削除のために現在の日時を設定
        db.session.commit()
        flash("削除しました", "success")
    except Exception as e:
        db.session.rollback()
        flash(str(e), "error")
    return redirect(url_for("reservation.reservations"))


@reservation.route("/update_room_choices", methods=["POST"])
def update_room_choices():
    data = request.get_json()
    checkin_date = data.get("checkin_date")
    checkout_date = data.get("checkout_date")

    checkin_date = datetime.strptime(checkin_date, "%Y-%m-%d").date()
    checkout_date = datetime.strptime(checkout_date, "%Y-%m-%d").date()

    reserved_room_ids = (
        db.session.query(Reservation.room_id)
        .filter(
            Reservation.checkin_date < checkout_date,
            Reservation.checkout_date > checkin_date,
            Reservation.deleted_at.is_(None),  # Exclude logically deleted reservations
        )
        .all()
    )
    reserved_room_ids = [r.room_id for r in reserved_room_ids]

    available_rooms = (
        Room.query.filter(~Room.id.in_(reserved_room_ids))
        .order_by(Room.room_number)
        .all()
    )

    rooms = [{"id": r.id, "room_number": r.room_number} for r in available_rooms]

    return jsonify({"rooms": rooms})
