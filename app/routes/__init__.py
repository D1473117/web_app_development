from flask import Blueprint

from .auth import bp as auth_bp
from .recipes import bp as recipes_bp
from .search import bp as search_bp
from .favorites import bp as favorites_bp
from .comments import bp as comments_bp
from .admin import bp as admin_bp
from .user import bp as user_bp

def register_blueprints(app):
    """
    註冊專案中所有的 Flask Blueprint
    """
    app.register_blueprint(recipes_bp)       # recipes 首頁路徑會是 / 
    app.register_blueprint(auth_bp)          # /auth/*
    app.register_blueprint(search_bp)        # /search/*
    app.register_blueprint(favorites_bp)     # /favorites/*
    app.register_blueprint(comments_bp)      # 掛載在 recipe 下的 comments
    app.register_blueprint(admin_bp)         # /admin/*
    app.register_blueprint(user_bp)          # /user/*
