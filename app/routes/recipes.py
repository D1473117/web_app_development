from flask import Blueprint, render_template, request, redirect, url_for, flash
# from flask_login import login_required, current_user
# from app.models.recipe import Recipe

bp = Blueprint('recipes', __name__)

@bp.route('/', methods=['GET'])
def index():
    """
    首頁／食譜列表。
    GET: 取得所有 is_public=True 的食譜，並依照建立時間排序。渲染 recipes/index.html。
    """
    pass

@bp.route('/recipes/<int:id>', methods=['GET'])
def detail(id):
    """
    食譜詳情頁。
    GET: 取得單筆食譜，及關聯的食材、留言。渲染 recipes/detail.html。
    """
    pass

@bp.route('/recipes/create', methods=['GET', 'POST'])
# @login_required
def create():
    """
    新增食譜。
    GET: 渲染 recipes/create.html 表單。
    POST: 接收並驗證表單資料，儲存圖片與食譜及食材，重導向到該食譜詳情頁。
    """
    pass

@bp.route('/recipes/<int:id>/edit', methods=['GET', 'POST'])
# @login_required
def edit(id):
    """
    編輯食譜。
    GET: 渲染 recipes/edit.html 並帶入舊資料。
    POST: 更新食譜內容。
    """
    pass

@bp.route('/recipes/<int:id>/update', methods=['POST'])
# @login_required
def update(id):
    """
    （可包含在 edit 裡面，或者單獨處理表單送出的 POST 重導向）
    此處作為接收表格更新處理的專屬路由。
    """
    pass

@bp.route('/recipes/<int:id>/delete', methods=['POST'])
# @login_required
def delete(id):
    """
    刪除食譜。
    POST: 確認身分為作者或管理員，刪除食譜資料，重導向至首頁或個人主頁。
    """
    pass
