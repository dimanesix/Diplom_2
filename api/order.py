import requests
import test_data


class OrderApi:
    def create_order(self, ingredients: list, access_token):
        data = {
            "ingredients": ingredients
        }
        response = requests.post(url=test_data.ORDERS_ENDPOINT, json=data, headers={"Authorization": access_token})
        return response

    def get_orders(self, access_token):
        response = requests.get(url=test_data.ORDERS_ENDPOINT, headers={"Authorization": access_token})
        return response
