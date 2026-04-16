from datetime import datetime
from flask_login import UserMixin
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
        user = User(email=email, password_hash=password_hash, is_admin=is_admin)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)
        
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
