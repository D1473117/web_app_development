from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.models.favorite import Favorite
from app.models.recipe import Recipe

bp = Blueprint('favorites', __name__, url_prefix='/favorites')

@bp.route('/toggle/<int:recipe_id>', methods=['POST'])
@login_required
def toggle_favorite(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        return jsonify({'status': 'error', 'message': '找不到此食譜'}), 404
        
    favorite = Favorite.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
    if favorite:
        favorite.delete()
        return jsonify({'status': 'success', 'action': 'removed'})
    else:
        Favorite.create(user_id=current_user.id, recipe_id=recipe_id)
        return jsonify({'status': 'success', 'action': 'added'})
