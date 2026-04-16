from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from . import db

class Favorite(db.Model):
    __tablename__ = 'favorites'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def create(user_id, recipe_id):
        """
        記錄一筆使用者的收藏。
        :param user_id: 使用者 ID
        :param recipe_id: 被收藏的食譜 ID
        :return: 成功回傳 Favorite，失敗 None
        """
        try:
            favorite = Favorite(user_id=user_id, recipe_id=recipe_id)
            db.session.add(favorite)
            db.session.commit()
            return favorite
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating favorite: {e}")
            return None

    @staticmethod
    def get_by_user(user_id):
        """取得特定使用者的所有收藏"""
        try:
            return Favorite.query.filter_by(user_id=user_id).all()
        except SQLAlchemyError as e:
            print(f"Error getting favorites: {e}")
            return []

    def delete(self):
        """取消收藏（刪除紀錄）"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting favorite: {e}")
            return False
