from flask import Blueprint, render_template, request
# from app.models.recipe import Recipe
# from app.models.ingredient import Ingredient

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=['GET'])
def search_keyword():
    """
    關鍵字搜尋。
    GET: 從 request.args 取得 'q'，模糊匹對食譜標題與描述，渲染 templates/search/results.html。
    """
    pass

@bp.route('/ingredients', methods=['GET'])
def search_ingredients():
    """
    食材反向搜尋。
    GET: 取得食材陣列清單，找出包含這些食材的食譜，依據比對符合度計算排序，渲染 results.html。
    """
    pass
