from flask import Blueprint, render_template, redirect, url_for, flash
# from app.models.user import User

bp = Blueprint('admin', __name__, url_prefix='/admin')

# 需定義 @admin_required 裝飾器邏輯或在此 Blueprint 使用 before_request 限制

@bp.route('/', methods=['GET'])
def dashboard():
    """
    後台總覽頁。
    GET: 顯示全站統計資料（食譜總數、用戶總數），渲染 templates/admin/dashboard.html。
    """
    pass

@bp.route('/users', methods=['GET'])
def manage_users():
    """
    管理區 - 使用者列表。
    GET: 渲染 templates/admin/users.html。
    """
    pass

@bp.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """
    刪除 / 停用使用者。
    POST: 刪除資料後 redirect admin.manage_users。
    """
    pass

@bp.route('/recipes', methods=['GET'])
def manage_recipes():
    """
    管理區 - 食譜列表審核。
    GET: 渲染 templates/admin/recipes.html。
    """
    pass

@bp.route('/comments/<int:comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    """
    刪除不當留言。
    POST: 管理員強制移除單一留言，重導向回到該食譜詳情。
    """
    pass
