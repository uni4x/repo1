# app/customer/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email


class CustomerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    address = TextAreaField("Address")
    phone = StringField("Phone")
    email = StringField("Email", validators=[DataRequired(), Email()])
    note = TextAreaField("Note")
    submit = SubmitField("Save")
