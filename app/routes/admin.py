from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.user import User
from app.models.recipe import Recipe
from app.models.comment import Comment

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.before_request
@login_required
def admin_required():
    if not current_user.is_admin:
        flash('您沒有權限存取此頁面', 'danger')
        return redirect(url_for('recipes.index'))

@bp.route('/', methods=['GET'])
def dashboard():
    users_count = User.query.count()
    recipes_count = Recipe.query.count()
    return render_template('admin/dashboard.html', users_count=users_count, recipes_count=recipes_count)

@bp.route('/users', methods=['GET'])
def manage_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    if user_id == current_user.id:
        flash('不能刪除自己的帳號', 'danger')
        return redirect(url_for('admin.manage_users'))
        
    user = User.query.get(user_id)
    if user:
        user.delete()
        flash('使用者已被刪除', 'success')
    return redirect(url_for('admin.manage_users'))

@bp.route('/recipes', methods=['GET'])
def manage_recipes():
    recipes = Recipe.query.all()
    return render_template('admin/recipes.html', recipes=recipes)

@bp.route('/comments/<int:comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        flash('找不到留言', 'danger')
        return redirect(url_for('admin.dashboard'))
        
    recipe_id = comment.recipe_id
    comment.delete()
    flash('留言已被刪除', 'success')
    return redirect(url_for('recipes.detail', id=recipe_id))
