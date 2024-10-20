import requests

import test_data


class IngredientsApi:
    def get_ingredients(self):
        response = requests.get(url=test_data.INGREDIENTS_ENDPOINT)
        return response