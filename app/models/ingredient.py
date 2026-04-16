from datetime import datetime
from . import db

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def create(name):
        ingredient = Ingredient(name=name)
        db.session.add(ingredient)
        db.session.commit()
        return ingredient

    @staticmethod
    def get_by_id(ingredient_id):
        return Ingredient.query.get(ingredient_id)
        
    @staticmethod
    def get_by_name(name):
        return Ingredient.query.filter_by(name=name).first()

    @staticmethod
    def get_all():
        return Ingredient.query.all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
