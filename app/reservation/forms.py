# app/reservation/forms.py

import sys
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import DateField, HiddenField, IntegerField, SelectField, StringField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from app import db
from app.models import Customer, Reservation, Room


class ReservationForm(FlaskForm):
    checkin_date = DateField(
        "チェックイン", format="%Y-%m-%d", validators=[DataRequired()]
    )
    checkout_date = DateField(
        "チェックアウト", format="%Y-%m-%d", validators=[DataRequired()]
    )
    customer_id = SelectField("お客様氏名", coerce=int, validators=[DataRequired()])
    room_id = SelectField("部屋番号", coerce=int, validators=[DataRequired()])
    payment_type = SelectField(
        "支払い方法",
        choices=[
            ("credit_card", "クレジットカード"),
            ("cash", "現金"),
            ("online", "オンライン"),
        ],
        validators=[DataRequired()],
    )
    payment_status = SelectField(
        "支払い状況",
        choices=[("paid", "支払済み"), ("pending", "未払い"), ("failed", "支払い失敗")],
        validators=[DataRequired()],
    )
    number_of_guests = IntegerField(
        "人数", validators=[DataRequired(), NumberRange(min=1)]
    )
    status = SelectField(
        "予約状況",
        choices=[
            ("confirmed", "予約確定"),
            ("checked_in", "チェックイン"),
            ("checked_out", "チェックアウト"),
        ],
        validators=[DataRequired()],
    )

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.customer_id.choices = [
            (c.id, c.name) for c in Customer.query.order_by(Customer.name).all()
        ]
        self.update_room_choices()

    def update_room_choices(self, checkin_date=None, checkout_date=None):
        if not checkin_date:
            checkin_date = datetime.today().date()
        if not checkout_date:
            checkout_date = datetime.today().date()

        reserved_room_ids = (
            db.session.query(Reservation.room_id)
            .filter(
                Reservation.checkin_date < checkout_date,
                Reservation.checkout_date > checkin_date,
                Reservation.deleted_at.is_(None),
            )
            .all()
        )
        reserved_room_ids = [r.room_id for r in reserved_room_ids]

        available_rooms = (
            Room.query.filter(~Room.id.in_(reserved_room_ids))
            .order_by(Room.room_number)
            .all()
        )

        self.room_id.choices = [(r.id, r.room_number) for r in available_rooms]
