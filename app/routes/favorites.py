from flask import Blueprint, jsonify, render_template
# from flask_login import login_required, current_user
# from app.models.favorite import Favorite

bp = Blueprint('favorites', __name__, url_prefix='/favorites')

@bp.route('/toggle/<int:recipe_id>', methods=['POST'])
# @login_required
def toggle_favorite(recipe_id):
    """
    切換食譜的收藏狀態。
    POST: 若已收藏則移除，若未收藏則新增。回傳 {"status": "success", "action": "added"|"removed"} (JSON)。
    """
    pass
