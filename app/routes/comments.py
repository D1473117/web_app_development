from flask import Blueprint, request, redirect, url_for, flash
# from flask_login import login_required, current_user
# from app.models.comment import Comment

bp = Blueprint('comments', __name__, url_prefix='/recipes/<int:recipe_id>/comments')

@bp.route('/', methods=['POST'])
# @login_required
def create_comment(recipe_id):
    """
    新增食譜留言與評分。
    POST: 接收 content 與 rating，建立留言並綁定 current_user 及 recipe_id。
    成功後 redirect 該食譜的詳情頁。
    """
    pass
