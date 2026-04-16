from flask import Blueprint, render_template
# from flask_login import login_required, current_user

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/profile', methods=['GET'])
# @login_required
def profile():
    """
    個人主頁。
    GET: 顯示自己建立的所有食譜、帳號數據。渲染 templates/user/profile.html。
    """
    pass

@bp.route('/favorites', methods=['GET'])
# @login_required
def favorites_list():
    """
    個人的收藏清單。
    GET: 列出所有已加入我的最愛的食譜。渲染 templates/user/favorites.html。
    """
    pass
