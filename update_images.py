from app import create_app
from app.models import db
from app.models.recipe import Recipe

app = create_app()

updates = {
    "番茄炒蛋": "tomato_egg.png",
    "香蒜培根義大利麵": "garlic_bacon_pasta.png",
    "日式咖哩雞": "japanese_curry.png",
    "香菇雞湯": "chicken_soup.png",
    "玉米濃湯": "corn_soup.png",
    "焦糖布丁": "caramel_flan.png",
    "清炒高麗菜": "stir_fried_cabbage.png",
    "紅燒肉": "braised_pork.png",
    "涼拌小黃瓜": "cucumber_salad.png",
    "麻婆豆腐": "mapo_tofu.png"
}

def update_images():
    with app.app_context():
        for title, filename in updates.items():
            recipe = Recipe.query.filter_by(title=title).first()
            if recipe:
                recipe.image_filename = filename
        db.session.commit()
        print("Updated image filenames successfully.")

if __name__ == '__main__':
    update_images()
