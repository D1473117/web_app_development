import sys
from app import create_app
from app.models import db
from app.models.user import User
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from werkzeug.security import generate_password_hash

app = create_app()

def seed_db():
    with app.app_context():
        # 建立資料表 (通常 app 啟動時或這裡初始化)
        db.create_all()

        # 找找看有沒有預設用戶，沒有的話建立一個
        user = User.query.filter_by(email='chef@test.com').first()
        if not user:
            user = User.create(
                email='chef@test.com',
                password_hash=generate_password_hash('password123'),
                is_admin=True
            )
            print("已建立預設主廚帳號：chef@test.com")

        recipes_data = [
            {
                "title": "番茄炒蛋",
                "description": "經典家常菜，酸甜開胃，非常下飯。",
                "steps": "1. 番茄切塊、雞蛋打散\n2. 熱鍋炒熟雞蛋，盛出備用\n3. 鍋中加油，下番茄炒出汁\n4. 加入雞蛋拌勻，加鹽或少許糖調味，起鍋。",
                "prep_time": 15,
                "difficulty": "Easy",
                "category": "主餐",
                "ingredients": ["番茄", "雞蛋", "鹽", "蔥"]
            },
            {
                "title": "香蒜培根義大利麵",
                "description": "簡單快速的義式料理，只需少量食材即可做出餐廳級美味。",
                "steps": "1. 煮一鍋熱水，加鹽，下義大利麵煮熟\n2. 培根切丁放入平底鍋煎出油脂\n3. 加入蒜末爆香\n4. 放入煮好的義大利麵、少許煮麵水拌炒\n5. 起鍋前撒上黑胡椒與起司粉。",
                "prep_time": 20,
                "difficulty": "Easy",
                "category": "主餐",
                "ingredients": ["義大利麵", "培根", "大蒜", "黑胡椒", "起司粉"]
            },
            {
                "title": "日式咖哩雞",
                "description": "濃郁柔滑的咖哩醬汁搭配滑嫩雞肉與爽口根莖類蔬菜。",
                "steps": "1. 馬鈴薯、胡蘿蔔、洋蔥切塊，雞腿肉切塊\n2. 熱鍋炒軟洋蔥，加入雞肉炒至變色\n3. 加入馬鈴薯與胡蘿蔔稍微拌炒，加水淹過食材\n4. 煮滾後轉小火燉煮約 15 分鐘直到蔬菜變軟\n5. 關火加入咖哩塊拌勻，再開小火煮至濃稠。",
                "prep_time": 45,
                "difficulty": "Medium",
                "category": "主餐",
                "ingredients": ["雞肉", "馬鈴薯", "胡蘿蔔", "洋蔥", "咖哩塊"]
            },
            {
                "title": "香菇雞湯",
                "description": "暖胃補氣的老火雞湯，香菇的鮮味完美融入湯中。",
                "steps": "1. 乾香菇泡軟，切去蒂頭；雞肉切塊汆燙去血水\n2. 準備一個燉鍋，放入雞肉、香菇、幾片薑\n3. 加入足量的水與少許米酒\n4. 煮滾後燉煮約 40 分鐘，起鍋前加鹽調味。",
                "prep_time": 60,
                "difficulty": "Easy",
                "category": "湯品",
                "ingredients": ["雞肉", "香菇", "薑", "米酒", "鹽"]
            },
            {
                "title": "玉米濃湯",
                "description": "小朋友最愛的甜香滑順濃湯，適合早餐或西餐配湯。",
                "steps": "1. 奶油熱鍋，加入麵粉炒成麵糊\n2. 分次加入牛奶與水慢慢攪拌均勻\n3. 加入玉米粒與火腿丁煮滾\n4. 淋入打散的蛋液，加入鹽和少許黑胡椒調味。",
                "prep_time": 20,
                "difficulty": "Easy",
                "category": "湯品",
                "ingredients": ["玉米", "牛奶", "雞蛋", "火腿", "奶油", "麵粉"]
            },
            {
                "title": "焦糖布丁",
                "description": "手工布丁，焦糖微苦甘甜搭配滑嫩蛋香，冰涼後更好吃。",
                "steps": "1. 糖加水煮至焦糖色，倒入模具底部\n2. 牛奶加熱稍微溫熱（不煮沸），加入適量糖攪拌融化\n3. 將雞蛋打散，慢慢倒入溫牛奶混合均勻，過篩兩次\n4. 將布丁液倒入模具，上方蓋上鋁箔紙\n5. 放入電鍋或烤箱水浴法蒸烤約 30 分鐘，冷藏後脫模。",
                "prep_time": 50,
                "difficulty": "Medium",
                "category": "甜點",
                "ingredients": ["雞蛋", "鮮奶", "砂糖"]
            },
            {
                "title": "清炒高麗菜",
                "description": "台式快炒店必備，青脆鮮甜的最佳家常蔬菜。",
                "steps": "1. 高麗菜洗淨手撕成片狀，大蒜拍碎\n2. 鍋中倒油，加入大蒜與少許辣椒爆香\n3. 大火快炒高麗菜，可加入少許水與米酒\n4. 起鍋前加鹽巴與鮮雞粉調味。",
                "prep_time": 10,
                "difficulty": "Easy",
                "category": "配菜",
                "ingredients": ["高麗菜", "大蒜", "鹽", "辣椒"]
            },
            {
                "title": "紅燒肉",
                "description": "肥而不膩口、醬香濃郁的經典紅燒肉，白飯殺手。",
                "steps": "1. 五花肉切塊，入鍋煎出豬油至表面微焦黃\n2. 加入薑片、八角、醬油、冰糖翻炒上色\n3. 倒入米酒與水淹過肉，大火煮滾\n4. 轉小火慢燉約 1 小時至肉質軟爛\n5. 大火收汁即可盛盤。",
                "prep_time": 90,
                "difficulty": "Hard",
                "category": "主餐",
                "ingredients": ["五花肉", "醬油", "冰糖", "八角", "薑", "米酒"]
            },
            {
                "title": "涼拌小黃瓜",
                "description": "夏天開胃首選，酸甜清脆，做法超簡單。",
                "steps": "1. 小黃瓜洗淨拍碎切大塊，加少許鹽醃製 10 分鐘後倒掉澀水\n2. 加入蒜末、辣椒末\n3. 加入白醋、糖、少許香油\n4. 攪拌均勻後放入冰箱冷藏 1 小時即可享用。",
                "prep_time": 15,
                "difficulty": "Easy",
                "category": "配菜",
                "ingredients": ["小黃瓜", "大蒜", "辣椒", "白醋", "糖", "香油"]
            },
            {
                "title": "麻婆豆腐",
                "description": "川菜代表之一，麻、辣、鮮、燙，極度下飯的豆腐料理。",
                "steps": "1. 嫩豆腐切塊稍微汆燙去豆腥味備用\n2. 鍋中熱油，下牛絞肉或豬絞肉炒散至變色\n3. 加入蒜末、薑末與辣豆瓣醬炒紅炒香\n4. 加入高湯或水，放入豆腐煮滾入味\n5. 加入花椒粉，用水澱粉勾芡，撒上蔥花即成。",
                "prep_time": 25,
                "difficulty": "Medium",
                "category": "主餐",
                "ingredients": ["嫩豆腐", "絞肉", "辣豆瓣醬", "花椒", "蒜", "蔥"]
            }
        ]

        recipe_count = 0
        for data in recipes_data:
            # 檢查是否已存在
            existing = Recipe.query.filter_by(title=data["title"]).first()
            if existing:
                continue
            
            # 建立關聯的食材
            ingredient_objs = []
            for ing_name in data["ingredients"]:
                ing = Ingredient.get_by_name(ing_name)
                if not ing:
                    ing = Ingredient(name=ing_name)
                    db.session.add(ing)
                    db.session.commit()
                ingredient_objs.append(ing)

            # 新增食譜
            new_recipe = Recipe(
                user_id=user.id,
                title=data["title"],
                description=data["description"],
                steps=data["steps"],
                prep_time=data["prep_time"],
                difficulty=data["difficulty"],
                category=data["category"],
                is_public=True
            )
            # 添加食材列表
            new_recipe.ingredients.extend(ingredient_objs)
            db.session.add(new_recipe)
            recipe_count += 1
        
        db.session.commit()
        print(f"成功新增了 {recipe_count} 道食譜與對應食材！")

if __name__ == '__main__':
    seed_db()
