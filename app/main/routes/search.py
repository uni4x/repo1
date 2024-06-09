# app/main/routes/search.py

from datetime import datetime

from flask import Blueprint, flash, render_template, request

from app import db

from ...models import Reservation, Room
from ..forms import SearchForm

bp = Blueprint("search", __name__)


@bp.route("/", methods=["GET", "POST"])
def search():
    form = SearchForm()
    available_rooms = None
    if form.validate_on_submit():
        checkin_date = form.checkin_date.data
        checkout_date = form.checkout_date.data

        # サーバー側での日付バリデーション
        if checkin_date < datetime.today().date():
            flash("チェックイン日は今日以降の日付を選択してください。", "error")
        elif checkout_date <= checkin_date:
            flash(
                "チェックアウト日はチェックイン日より後の日付を選択してください。",
                "error",
            )
        else:
            # 空室検索クエリ
            available_rooms = (
                Room.query.filter(Room.status == "available")
                .filter(
                    # チェックアウト日が検索期間外の部屋
                    Room.id.notin_(
                        db.session.query(Reservation.room_id).filter(
                            (Reservation.checkin_date <= checkout_date)
                            & (Reservation.checkout_date >= checkin_date)
                            & (Reservation.deleted_at.is_(None))
                            & (Reservation.completed_at.is_(None))
                        )
                    )
                )
                .all()
            )
            return render_template(
                "search.html", form=form, available_rooms=available_rooms
            )
    return render_template("search.html", form=form, available_rooms=available_rooms)
