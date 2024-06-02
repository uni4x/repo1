# app/__init__.py

from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_wtf.csrf import CSRFProtect, CSRFError
from config import config
from flask_migrate import Migrate
from flask_login import LoginManager
from app.error_handlers import register_error_handlers
import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv

# .envファイルをロード
load_dotenv()

db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name='default'):
    app = Flask(__name__)  # インスタンス作成

    # 環境変数FLASK_CONFIGから設定を読み込み
    config_name = config_name or os.getenv('FLASK_CONFIG') or 'default'
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # 各種Blueprint（モジュール）の登録 
    from .roomtype import roomtype as roomtype_blueprint
    app.register_blueprint(roomtype_blueprint, url_prefix='/roomtype')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .employee import employee as employee_blueprint
    app.register_blueprint(employee_blueprint, url_prefix='/employee')

    from .routes import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .room import room as room_blueprint
    app.register_blueprint(room_blueprint, url_prefix='/room')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/main')
    # app.register_blueprint(main_blueprint)

    from .customer import customer as customer_blueprint
    app.register_blueprint(customer_blueprint, url_prefix='/customer')

    from .reservation import reservation as reservation_blueprint
    app.register_blueprint(reservation_blueprint, url_prefix='/reservation')

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        db.session.rollback()
        return render_template('error.html', message='データベースエラーが発生しました。詳細: ' + str(error.orig)), 400

    @app.errorhandler(Exception)
    def handle_exception(error):
        db.session.rollback()
        return render_template('error.html', message='予期しないエラーが発生しました。詳細: ' + str(error)), 500

    register_error_handlers(app, db)

    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('App startup')

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import Employee
    return Employee.query.get(int(user_id))

