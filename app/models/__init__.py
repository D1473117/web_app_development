from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .recipe import Recipe, recipe_ingredients
from .ingredient import Ingredient
from .favorite import Favorite
from .comment import Comment
