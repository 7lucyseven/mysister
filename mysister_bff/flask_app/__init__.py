from flask import Flask
from flask_app.main_flask import app as main_blueprint
from conf import Config

def create_app():
    app = Flask(__name__)

    # Blueprintの登録
    app.register_blueprint(main_blueprint)

    # 設定ファイルの読み込み
    app.config.from_object(Config)

    return app
