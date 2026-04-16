import os
from flask import Flask
from .models import db
from .routes import register_blueprints
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = "請先登入以存取此頁面"
login_manager.login_message_category = "warning"

def create_app(config_class=None):
    """應用程式 Factory Function"""
    app = Flask(__name__)
    
    # 載入設定
    if config_class is None:
        from config import Config
        app.config.from_object(Config)
    else:
        app.config.from_object(config_class)

    # 確保 instance 目錄存在 (存放 SQLite DB)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 確保上傳目錄存在
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except OSError:
        pass

    # 初始化 Extensions
    db.init_app(app)
    login_manager.init_app(app)

    # 設定 Flask-Login user_loader
    @login_manager.user_loader
    def load_user(user_id):
        from .models.user import User
        return User.query.get(int(user_id))

    # 註冊所有 Router Blueprints
    register_blueprints(app)

    return app
