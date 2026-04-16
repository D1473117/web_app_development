from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from . import db

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def create(**kwargs):
        """
        新增一筆食譜留言與評分。
        :param kwargs: 包含 content, rating, user_id, recipe_id
        :return: 成功回傳 Comment，失敗 None
        """
        try:
            comment = Comment(**kwargs)
            db.session.add(comment)
            db.session.commit()
            return comment
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating comment: {e}")
            return None

    @staticmethod
    def get_by_id(comment_id):
        """根據 ID 取得單筆留言"""
        try:
            return Comment.query.get(comment_id)
        except SQLAlchemyError as e:
            print(f"Error getting comment: {e}")
            return None
        
    @staticmethod
    def get_by_recipe(recipe_id):
        """取得某食譜底下的所有留言"""
        try:
            return Comment.query.filter_by(recipe_id=recipe_id).all()
        except SQLAlchemyError as e:
            print(f"Error getting recipe comments: {e}")
            return []

    def update(self, **kwargs):
        """更新留言內容"""
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
            return self
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating comment: {e}")
            return None

    def delete(self):
        """刪除留言"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting comment: {e}")
            return False
