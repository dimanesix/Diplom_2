from api.ingredients import IngredientsApi
import random


class Helpers:
    def get_random_existing_ingredient(self):
        # в предпосылке, что функция получения ингредиентов работает без ошибок
        # иначе составляем вручную список и помещаем его в test_data.py
        response = IngredientsApi().get_ingredients()
        ingredients: list = response.json()["data"]
        ingredients_db = []
        for ingredient in ingredients:
            ingredients_db.append((ingredient["_id"], ingredient["name"]))
        random_ingredient = random.choice(ingredients_db)
        return random_ingredient
