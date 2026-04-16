from datetime import datetime
from . import db

class Favorite(db.Model):
    __tablename__ = 'favorites'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def create(user_id, recipe_id):
        favorite = Favorite(user_id=user_id, recipe_id=recipe_id)
        db.session.add(favorite)
        db.session.commit()
        return favorite

    @staticmethod
    def get_by_user(user_id):
        return Favorite.query.filter_by(user_id=user_id).all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
