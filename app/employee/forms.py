# employee/forms.py

from flask_wtf import FlaskForm
from wtforms import (
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
    ValidationError,
)
from wtforms.validators import DataRequired, EqualTo, Length


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=100)])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("confirm_password", message="Passwords must match."),
        ],
    )
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class EmployeeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField("Description", default="")
    submit = SubmitField("Submit")
