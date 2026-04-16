from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.recipe import Recipe
from app.models.favorite import Favorite

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    my_recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    return render_template('user/profile.html', recipes=my_recipes)

@bp.route('/favorites', methods=['GET'])
@login_required
def favorites_list():
    favorites = Favorite.get_by_user(current_user.id)
    recipes = [f.recipe for f in favorites if f.recipe]
    return render_template('user/favorites.html', recipes=recipes)
