from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('信箱與密碼為必填欄位', 'danger')
            return render_template('auth/register.html')
            
        if User.query.filter_by(email=email).first():
            flash('此信箱已被註冊', 'danger')
            return render_template('auth/register.html')
            
        hashed_password = generate_password_hash(password)
        User.create(email=email, password_hash=hashed_password)
        
        flash('註冊成功！請登入', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('登入成功！', 'success')
            return redirect(url_for('recipes.index'))
        else:
            flash('請檢查您的信箱或密碼再試一次', 'danger')
            
    return render_template('auth/login.html')

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('您已成功登出', 'info')
    return redirect(url_for('recipes.index'))
