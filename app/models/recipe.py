from datetime import datetime
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
        recipe = Recipe(**kwargs)
        db.session.add(recipe)
        db.session.commit()
        return recipe

    @staticmethod
    def get_by_id(recipe_id):
        return Recipe.query.get(recipe_id)

    @staticmethod
    def get_all(public_only=True):
        if public_only:
            return Recipe.query.filter_by(is_public=True).all()
        return Recipe.query.all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
