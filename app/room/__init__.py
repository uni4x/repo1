# app/room/__init__.py

from flask import Blueprint

# Blueprintを定義（インスタンスを作成）
room = Blueprint('room', __name__, template_folder='templates', static_folder='static', static_url_path='/room/static')

from . import routes

# BlueprintはFlaskのモジュール化の手段
# room というBlueprintが定義（作成）されている
# このBlueprintは、ルートディレクトリからのアクセスはできない
# そのため、ルートディレクトリからのアクセスは、room.indexというように、roomをつけてアクセスする

# my_blueprint = Blueprint('my_blueprint', __name__)
# 第一引数はBlueprintの名前、第二引数はこのBlueprintが定義されているモジュールまたはパッケージ