import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """應用程式的基礎設定"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key-for-dev')
    
    # SQLite 資料庫預設存放在 instance/ 目錄
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'database.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 圖片上傳設定
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 限制最大上傳為 5MB
