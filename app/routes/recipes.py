import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from app.models import db

bp = Blueprint('recipes', __name__)

@bp.route('/', methods=['GET'])
def index():
    recipes = Recipe.get_all(public_only=True)
    return render_template('recipes/index.html', recipes=recipes)

@bp.route('/recipes/<int:id>', methods=['GET'])
def detail(id):
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜', 'danger')
        return redirect(url_for('recipes.index'))
    return render_template('recipes/detail.html', recipe=recipe)

@bp.route('/recipes/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        steps = request.form.get('steps')
        prep_time = request.form.get('prep_time')
        difficulty = request.form.get('difficulty')
        category = request.form.get('category')
        is_public = request.form.get('is_public') == 'on'
        
        if not title or not steps:
            flash('「標題」與「步驟」為必填欄位', 'danger')
            return render_template('recipes/create.html')
            
        file = request.files.get('image')
        filename = None
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            
        recipe = Recipe.create(
            user_id=current_user.id,
            title=title,
            description=description,
            steps=steps,
            prep_time=int(prep_time) if prep_time else None,
            difficulty=difficulty,
            category=category,
            image_filename=filename,
            is_public=is_public
        )
        
        ingredients_input = request.form.get('ingredients')
        if ingredients_input and recipe:
            for name in ingredients_input.split(','):
                name = name.strip()
                if name:
                    ingredient = Ingredient.get_by_name(name) or Ingredient.create(name=name)
                    recipe.ingredients.append(ingredient)
            db.session.commit()
            
        flash('成功新增食譜！', 'success')
        return redirect(url_for('recipes.detail', id=recipe.id))
        
    return render_template('recipes/create.html')

@bp.route('/recipes/<int:id>/edit', methods=['GET'])
@login_required
def edit(id):
    recipe = Recipe.get_by_id(id)
    if not recipe or (recipe.user_id != current_user.id and not current_user.is_admin):
        flash('沒有權限編輯此食譜', 'danger')
        return redirect(url_for('recipes.index'))
        
    return render_template('recipes/edit.html', recipe=recipe)

@bp.route('/recipes/<int:id>/update', methods=['POST'])
@login_required
def update(id):
    recipe = Recipe.get_by_id(id)
    if not recipe or (recipe.user_id != current_user.id and not current_user.is_admin):
        flash('沒有權限更新此食譜', 'danger')
        return redirect(url_for('recipes.index'))
        
    title = request.form.get('title')
    steps = request.form.get('steps')
    
    if not title or not steps:
        flash('「標題」與「步驟」為必填欄位', 'danger')
        return redirect(url_for('recipes.edit', id=id))
        
    file = request.files.get('image')
    filename = recipe.image_filename
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        
    prep_time = request.form.get('prep_time')
    recipe.update(
        title=title,
        description=request.form.get('description'),
        steps=steps,
        prep_time=int(prep_time) if prep_time else None,
        difficulty=request.form.get('difficulty'),
        category=request.form.get('category'),
        image_filename=filename,
        is_public=(request.form.get('is_public') == 'on')
    )
    
    ingredients_input = request.form.get('ingredients')
    if ingredients_input is not None:
        recipe.ingredients.clear()
        for name in ingredients_input.split(','):
            name = name.strip()
            if name:
                ingredient = Ingredient.get_by_name(name) or Ingredient.create(name=name)
                recipe.ingredients.append(ingredient)
        db.session.commit()
    
    flash('食譜更新成功！', 'success')
    return redirect(url_for('recipes.detail', id=id))

@bp.route('/recipes/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    recipe = Recipe.get_by_id(id)
    if not recipe or (recipe.user_id != current_user.id and not current_user.is_admin):
        flash('沒有權限刪除此食譜', 'danger')
        return redirect(url_for('recipes.index'))
        
    recipe.delete()
    flash('食譜已被刪除', 'info')
    return redirect(url_for('user.profile'))
