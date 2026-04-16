from flask import Blueprint, render_template, request, redirect, url_for, flash
# from app.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理使用者註冊。
    GET: 渲染 templates/auth/register.html 表單。
    POST: 接收 Email 與密碼，驗證後建立新 User，重導向到登入頁。
    """
    pass

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理使用者登入。
    GET: 渲染 templates/auth/login.html。
    POST: 驗證帳號密碼，成功則呼叫 login_user，重導向到首頁。
    """
    pass

@bp.route('/logout', methods=['POST'])
def logout():
    """
    處理使用者登出。
    POST: 呼叫 logout_user，清除 session 後重導向到首頁。
    """
    pass
