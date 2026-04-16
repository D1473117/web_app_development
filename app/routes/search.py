from flask import Blueprint, render_template, request
from sqlalchemy import or_
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=['GET'])
def search_keyword():
    query = request.args.get('q', '')
    if query:
        recipes = Recipe.query.filter(
            Recipe.is_public == True,
            or_(Recipe.title.contains(query), Recipe.description.contains(query))
        ).all()
    else:
        recipes = []
    
    return render_template('search/results.html', recipes=recipes, query=query)

@bp.route('/ingredients', methods=['GET'])
def search_ingredients():
    q = request.args.get('q', '')
    if not q:
        return render_template('search/results.html', recipes=[], query='')
        
    keywords = [k.strip() for k in q.split(',') if k.strip()]
    if not keywords:
        return render_template('search/results.html', recipes=[], query=q)
        
    recipes_set = set()
    for kw in keywords:
        # 使用 contains 找出部分吻合的食材
        ingredients = Ingredient.query.filter(Ingredient.name.contains(kw)).all()
        for ingredient in ingredients:
            for recipe in ingredient.recipes:
                if recipe.is_public:
                    recipes_set.add(recipe)
                    
    recipes = list(recipes_set)
    return render_template('search/results.html', recipes=recipes, query=q)
