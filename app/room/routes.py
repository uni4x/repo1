# app/room/routes.py

from flask import flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

from app import db

from ..models import Room, RoomType
from . import room
from .forms import RoomForm


@room.route("/rooms", defaults={"id": None}, methods=["GET", "POST"])
@room.route("/rooms/<int:id>", methods=["GET", "POST"])
@login_required
def rooms(id):
    if id:
        room = Room.query.get_or_404(id)
        form = RoomForm(request.form, obj=room)
    else:
        room = Room()
        form = RoomForm(request.form)

    if request.args.get("mode") == "json":
        room = Room.query.get_or_404(id)
        return jsonify(
            {
                "id": room.id,
                "room_number": room.room_number,
                "room_type_id": room.room_type_id,
                "price": room.price,
                "status": room.status,
            }
        )

    if request.method == "POST":
        if form.validate():
            form.populate_obj(room)
            try:
                if not id:
                    db.session.add(room)
                db.session.commit()
                flash("部屋情報が保存されました。", "success")
            except IntegrityError as e:
                db.session.rollback()
                error_message = "データベースエラー: "
                if "UNIQUE constraint failed" in str(e.orig):
                    error_message += "部屋番号が既に存在します。"
                else:
                    error_message += "不明なエラーが発生しました。"
                flash(error_message, "error")
                return redirect(url_for("room.rooms", id=id))
            except Exception as e:
                db.session.rollback()
                flash(f"予期しないエラーが発生しました: {str(e)}", "error")
                return redirect(url_for("room.rooms", id=id))
            return redirect(url_for("room.rooms"))
        else:
            flash("入力値に問題があります。", "error")

    query = Room.query

    search_room_number = request.args.get("search_room_number")
    if search_room_number:
        query = query.filter(Room.room_number.contains(search_room_number))

    search_status = request.args.get("search_status")
    if search_status:
        query = query.filter(Room.status == search_status)

    sort_order = request.args.get("sort_order", "asc")
    if sort_order == "asc":
        query = query.order_by(Room.room_number.asc())
    else:
        query = query.order_by(Room.room_number.desc())

    page = request.args.get("page", 1, type=int)
    per_page = 5
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    rooms = pagination.items

    return render_template(
        "room.html",
        rooms=rooms,
        pagination=pagination,
        sort_order=sort_order,
        form=form,
        id=id,
    )


@room.route("/room/<int:id>", methods=["POST"])
def delete_room(id):
    try:
        room = Room.query.get_or_404(id)
        db.session.delete(room)
        db.session.commit()
        flash("削除しました", "success")
    except Exception as e:
        db.session.rollback()
        flash(str(e), "error")
    return redirect(url_for("room.rooms"))
