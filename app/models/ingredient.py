from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from . import db

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def create(name):
        """
        新增一筆食材標籤。
        :param name: 食材名稱
        :return: 成功回傳 Ingredient，失敗 None
        """
        try:
            ingredient = Ingredient(name=name)
            db.session.add(ingredient)
            db.session.commit()
            return ingredient
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating ingredient: {e}")
            return None

    @staticmethod
    def get_by_id(ingredient_id):
        """取得單一食材"""
        try:
            return Ingredient.query.get(ingredient_id)
        except SQLAlchemyError as e:
            print(f"Error getting ingredient: {e}")
            return None
        
    @staticmethod
    def get_by_name(name):
        """靠名稱尋找食材（確保唯一性）"""
        try:
            return Ingredient.query.filter_by(name=name).first()
        except SQLAlchemyError as e:
            print(f"Error getting ingredient by name: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有食材清單"""
        try:
            return Ingredient.query.all()
        except SQLAlchemyError as e:
            print(f"Error getting ingredients: {e}")
            return []

    def update(self, **kwargs):
        """更新食材屬性"""
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
            return self
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating ingredient: {e}")
            return None

    def delete(self):
        """刪除食材此標籤"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting ingredient: {e}")
            return False
