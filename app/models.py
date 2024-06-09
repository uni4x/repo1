# app/models.py

from app import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))


# Customer モデル
class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=False)
    note = db.Column(db.Text)
    deleted_at = db.Column(db.DateTime, nullable=True)

    reservations = db.relationship("Reservation", backref="customer", lazy=True)


# Reservation モデル
class Reservation(db.Model):
    __tablename__ = "reservation"
    id = db.Column(db.Integer, primary_key=True)
    checkin_date = db.Column(db.Date, nullable=False)
    checkout_date = db.Column(db.Date, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)
    payment_type = db.Column(db.String(50))
    payment_status = db.Column(db.String(50))  # 例: 'paid', 'unpaid'
    number_of_guests = db.Column(db.Integer, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)  # キャンセル
    status = db.Column(db.String(50), nullable=False, default="confirmed")  # 予約の状態
    completed_at = db.Column(db.DateTime, nullable=True)  # 予約完了、チェックアウト

    room = db.relationship("Room", lazy=True)


# Room モデル
class Room(db.Model):
    __tablename__ = "room"
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), nullable=False, unique=True)
    room_type_id = db.Column(db.Integer, db.ForeignKey("room_type.id"), nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="available")
    room_type = db.relationship("RoomType", backref="rooms", lazy=True)


# RoomType モデル
class RoomType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))


# Employee モデル
class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(256))
    description = db.Column(db.Text, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_active(self):
        return self.deleted_at is None
