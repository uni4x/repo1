# app/room/forms.py

from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SelectField, StringField
from wtforms.validators import DataRequired, Length

from app.models import RoomType


class RoomForm(FlaskForm):
    room_number = StringField(
        "Room Number", validators=[DataRequired(), Length(max=10)]
    )  # 部屋番号を追加
    room_type_id = SelectField("Room Type", coerce=int, validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    status = SelectField(
        "Status",
        choices=[
            ("available", "Available"),
            ("reserved", "Reserved"),
            ("occupied", "Occupied"),
            ("maintenance", "Maintenance"),
            ("cleaning", "Cleaning"),
        ],
        validators=[DataRequired()],
    )

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.room_type_id.choices = [
            (rt.id, rt.type_name)
            for rt in RoomType.query.order_by(RoomType.type_name).all()
        ]
