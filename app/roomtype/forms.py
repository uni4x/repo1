from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class RoomTypeForm(FlaskForm):
    type_name = StringField("Room Type Name", default="", validators=[DataRequired()])
    description = TextAreaField("Description", default="")
    submit = SubmitField("Submit")
