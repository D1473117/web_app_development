from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.exc import SQLAlchemyError
from . import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 關聯
    recipes = db.relationship('Recipe', backref='author', lazy=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    @staticmethod
    def create(email, password_hash, is_admin=False):
        """
        新增一位使用者。
        :param email: 使用者信箱
        :param password_hash: 雜湊後的密碼
        :param is_admin: 是否為管理員
        :return: 成功回傳 User 物件，失敗回傳 None
        """
        try:
            user = User(email=email, password_hash=password_hash, is_admin=is_admin)
            db.session.add(user)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def get_by_id(user_id):
        """
        以 ID 取得單筆使用者記錄。
        :param user_id: 使用者 ID
        :return: User 物件或 None
        """
        try:
            return User.query.get(user_id)
        except SQLAlchemyError as e:
            print(f"Error getting user by id: {e}")
            return None
            
    def update(self, **kwargs):
        """
        更新使用者的屬性。
        :param kwargs: 欲更新的欄位與值
        :return: 成功回傳 User，失敗回傳 None
        """
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
            return self
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating user: {e}")
            return None

    def delete(self):
        """
        刪除此使用者。
        :return: 成功 True，失敗 False
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting user: {e}")
            return False
