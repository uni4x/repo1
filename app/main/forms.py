# app/main/forms.py
from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange, Regexp


class SearchForm(FlaskForm):
    checkin_date = DateField(
        "チェックイン", format="%Y-%m-%d", validators=[DataRequired()]
    )
    checkout_date = DateField(
        "チェックアウト", format="%Y-%m-%d", validators=[DataRequired()]
    )
    submit = SubmitField("空室検索")


class ReservationForm(FlaskForm):
    submit = SubmitField("この部屋を予約する")


class CustomerInfoForm(FlaskForm):
    name = StringField(
        "お名前", validators=[DataRequired(message="名前は必須項目です。")]
    )
    address = StringField(
        "ご住所", validators=[DataRequired(message="住所は必須項目です。")]
    )
    phone = StringField(
        "お電話番号（ハイフンなし、半角数字でご入力ください）",
        validators=[
            DataRequired(message="電話番号は必須項目です。"),
            Regexp(
                r"^\d{8,12}$",
                message="電話番号は8桁以上12桁以下の数字（ハイフンなし）で入力してください。",
            ),
        ],
    )
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired(message="メールアドレスは必須項目です。"),
            Email(message="有効なメールアドレスを入力してください。"),
        ],
    )
    number_of_guests = IntegerField(
        "ご宿泊のご予定人数",
        validators=[
            DataRequired(message="予定人数は必須項目です。"),
            NumberRange(min=1, message="予定人数は1人以上である必要があります。"),
        ],
    )
    note = StringField("備考")
    payment_type = SelectField(
        "お支払い方法",
        choices=[
            ("credit_card", "クレジットカード"),
            ("cash", "現金"),
            ("online", "オンライン"),
        ],
        validators=[DataRequired(message="支払い方法は必須項目です。")],
    )
    submit = SubmitField("この内容で予約する")


class ConfirmationForm(FlaskForm):
    submit = SubmitField("予約を確定する")
