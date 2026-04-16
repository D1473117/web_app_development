from app import create_app
from app.models import db

app = create_app()

if __name__ == '__main__':
    # 啟動時自動建立未存在的資料表
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
