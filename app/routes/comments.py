from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.comment import Comment
from app.models.recipe import Recipe

bp = Blueprint('comments', __name__, url_prefix='/recipes/<int:recipe_id>/comments')

@bp.route('/', methods=['POST'])
@login_required
def create_comment(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        flash('找不到食譜', 'danger')
        return redirect(url_for('recipes.index'))
        
    content = request.form.get('content')
    rating = request.form.get('rating')
    
    if not content:
        flash('留言內容不能為空', 'danger')
        return redirect(url_for('recipes.detail', id=recipe_id))
        
    Comment.create(
        content=content,
        rating=int(rating) if rating else None,
        user_id=current_user.id,
        recipe_id=recipe_id
    )
    flash('留言已新增', 'success')
    return redirect(url_for('recipes.detail', id=recipe_id))
