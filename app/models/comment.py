from datetime import datetime
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
        comment = Comment(**kwargs)
        db.session.add(comment)
        db.session.commit()
        return comment

    @staticmethod
    def get_by_id(comment_id):
        return Comment.query.get(comment_id)
        
    @staticmethod
    def get_by_recipe(recipe_id):
        return Comment.query.filter_by(recipe_id=recipe_id).all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
