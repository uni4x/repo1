# app/roomtype/routes.py

from flask import flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from app import db

from ..models import Reservation, Room, RoomType
from . import roomtype
from .forms import RoomTypeForm


# 新規登録、一覧、編集
@roomtype.route("/room_types", defaults={"id": None}, methods=["GET", "POST"])
@roomtype.route("/room_types/<int:id>", methods=["GET", "POST"])
@login_required
def room_types(id):
    # idがある場合は編集、ない場合は新規登録
    if id:
        room_type = RoomType.query.get_or_404(id)
        form = RoomTypeForm(request.form, obj=room_type)
    else:
        room_type = RoomType()
        form = RoomTypeForm(request.form)

    # JSONデータを要求する場合
    if request.args.get("mode") == "json":
        room_type = RoomType.query.get_or_404(id)
        return jsonify(
            {
                "id": room_type.id,
                "type_name": room_type.type_name,
                "description": room_type.description,
            }
        )

    # POSTでデータが送信された場合
    if request.method == "POST":
        if form.validate():
            form.populate_obj(room_type)
            if not id:
                db.session.add(room_type)  # 新規登録の場合、先に追加
            if id:
                room_type.type_name = request.form["type_name2"]
                room_type.description = request.form["description2"]
            db.session.commit()
            return redirect(url_for("roomtype.room_types"))
        else:
            flash("入力値に問題があります。", "error")

    # GETリクエストの場合、idがあればそのデータをフォームにロード
    else:
        if id:
            room_type = RoomType.query.get(id) if id else RoomType()
            form = RoomTypeForm(obj=room_type)

    # 検索クエリの初期設定
    query = RoomType.query

    # type_nameに基づくフィルタリング条件の適用
    search_type = request.args.get("search_type")
    if search_type:
        query = query.filter(RoomType.type_name.contains(search_type))

    # descriptionに基づくフィルタリング条件の適用
    search_description = request.args.get("search_description")
    if search_description:
        query = query.filter(RoomType.description.contains(search_description))

    # ソートオーダーの取得と適用
    sort_order = request.args.get("sort_order", "asc")
    if sort_order == "asc":
        query = query.order_by(RoomType.type_name.asc())
    else:
        query = query.order_by(RoomType.type_name.desc())

    # ページネーションの設定
    page = request.args.get("page", 1, type=int)
    per_page = 5
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    room_types = pagination.items

    return render_template(
        "room_type.html",
        room_types=room_types,
        pagination=pagination,
        sort_order=sort_order,
        form=form,
        id=id,
    )


# 削除用のルート
@roomtype.route("/room_type/<int:id>", methods=["POST"])
def delete_room_type(id):
    try:
        room_type = RoomType.query.get_or_404(id)
        db.session.delete(room_type)
        db.session.commit()
        flash("削除しました", "success")
    except Exception as e:
        db.session.rollback()
        flash(str(e), "error")
    return redirect(url_for("roomtype.room_types"))
