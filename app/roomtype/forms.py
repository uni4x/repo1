from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class RoomTypeForm(FlaskForm):
    type_name = StringField("Room Type Name", default="", validators=[DataRequired()])
    description = TextAreaField("Description", default="")
    submit = SubmitField("Submit")
