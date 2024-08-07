# データベースを初期化

from app import create_app, db
from app.models import Customer, Employee, Reservation, Room, RoomType


def initialize_db():
    app = create_app("development")
    with app.app_context():
        print("Creating all tables...")
        db.drop_all()  # データベースをリセットする場合はこの行を追加
        db.create_all()
        print("Database initialized!")


if __name__ == "__main__":
    initialize_db()
