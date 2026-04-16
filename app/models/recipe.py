from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from . import db

recipe_ingredients = db.Table('recipe_ingredients',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
)

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    steps = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.Integer)
    difficulty = db.Column(db.String(50))
    category = db.Column(db.String(50))
    image_filename = db.Column(db.String(255))
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 多對多關聯 - 食材
    ingredients = db.relationship('Ingredient', secondary=recipe_ingredients, lazy='subquery',
        backref=db.backref('recipes', lazy=True))
    
    # 關聯留言與收藏
    comments = db.relationship('Comment', backref='recipe', lazy=True, cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', backref='recipe', lazy=True, cascade='all, delete-orphan')

    @staticmethod
    def create(**kwargs):
        """
        新增食譜記錄。
        :param kwargs: 食譜對應欄位
        :return: 成功回傳 Recipe，失敗回傳 None
        """
        try:
            recipe = Recipe(**kwargs)
            db.session.add(recipe)
            db.session.commit()
            return recipe
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating recipe: {e}")
            return None

    @staticmethod
    def get_by_id(recipe_id):
        """
        取得單筆食譜記錄。
        :param recipe_id: 食譜 ID
        :return: Recipe 物件或 None
        """
        try:
            return Recipe.query.get(recipe_id)
        except SQLAlchemyError as e:
            print(f"Error getting recipe: {e}")
            return None

    @staticmethod
    def get_all(public_only=True):
        """
        取得所有食譜清單。
        :param public_only: 預設 True，只回傳公開的食譜
        :return: 食譜串列
        """
        try:
            if public_only:
                return Recipe.query.filter_by(is_public=True).all()
            return Recipe.query.all()
        except SQLAlchemyError as e:
            print(f"Error getting recipes: {e}")
            return []

    def update(self, **kwargs):
        """
        更新食譜記錄。
        :param kwargs: 更新的欄位值
        :return: 成功回傳 Recipe，失敗 None
        """
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            self.updated_at = datetime.utcnow()
            db.session.commit()
            return self
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating recipe: {e}")
            return None

    def delete(self):
        """
        刪除食譜。
        :return: 成功 True，失敗 False
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting recipe: {e}")
            return False
