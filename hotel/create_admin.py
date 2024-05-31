# hotel/create_admin.py

from app import create_app, db
from app.models import Employee
from werkzeug.security import generate_password_hash

# Flaskアプリケーションを作成
app = create_app()

with app.app_context():
    # 管理者アカウントの詳細を設定
    admin_name = 'admin'
    admin_password = 'admin_password'
    admin_description = 'This is the admin account.'

    # パスワードをハッシュ化
    hashed_password = generate_password_hash(admin_password)

    # 管理者アカウントを作成
    admin = Employee(name=admin_name, password_hash=hashed_password, description=admin_description, is_admin=True)

    # データベースに追加
    db.session.add(admin)
    db.session.commit()

    print('管理者アカウントが作成されました。')
