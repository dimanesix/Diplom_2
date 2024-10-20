import allure
import pytest
from faker import Faker

from api.order import OrderApi
from helpers import Helpers


class TestCreateOrder:
    @allure.title('Проверка создания заказа с авторизацией')
    @pytest.mark.parametrize('register_user', [(Faker().free_email(), Faker().password(), Faker().first_name())],
                             indirect=True)
    def test_create_order_with_auth(self, register_user):
        _, email, password, name = register_user
        access_token = _.json()["accessToken"]
        ingredient = Helpers().get_random_existing_ingredient()
        with allure.step("Сделать заказ от авторизованного пользователя"):
            response = OrderApi().create_order([ingredient[0]], access_token)
        assert (response.status_code == 200 and
                response.json()["success"] is True and
                isinstance(response.json()["name"], str) and
                response.json()["order"]["ingredients"][0]["_id"] == ingredient[0] and
                response.json()["order"]["ingredients"][0]["name"] == ingredient[1] and
                response.json()["order"]["owner"]["name"] == name and
                response.json()["order"]["owner"]["email"] == email and
                isinstance(response.json()["order"]["number"], int)), ('Ошибка при создании заказа от авторизованного '
                                                                       'пользователя!')

    @allure.title('Проверка создания заказа без авторизации')
    def test_create_order_without_auth(self):
        access_token = None
        ingredient = Helpers().get_random_existing_ingredient()
        with allure.step("Сделать заказ от неавторизованного пользователя"):
            response = OrderApi().create_order([ingredient[0]], access_token)
        assert (response.status_code == 200 and
                response.json()["success"] is True and
                isinstance(response.json()["name"], str) and
                isinstance(response.json()["order"]["number"], int)), ('Ошибка при создании заказа от неавторизованного'
                                                                       'пользователя!')

    @allure.title('Проверка создания заказа с несколькими ингредиентами')
    def test_create_order_with_some_ingredients(self):
        access_token = None
        first_ingredient = Helpers().get_random_existing_ingredient()
        second_ingredient = Helpers().get_random_existing_ingredient()
        with allure.step("Сделать заказ с несколькими ингредиентами"):
            response = OrderApi().create_order([first_ingredient[0], second_ingredient[0]], access_token)
        assert (response.status_code == 200 and
                response.json()["success"] is True and
                isinstance(response.json()["name"], str) and
                isinstance(response.json()["order"]["number"], int)), ('Ошибка при создании заказа с несколькими '
                                                                       'ингредиентами!')

    @allure.title('Проверка создания заказа без ингредиентов')
    def test_create_order_without_ingredients(self):
        access_token = None
        ingredients = []
        with allure.step("Сделать заказ без ингредиентов"):
            response = OrderApi().create_order(ingredients, access_token)
        assert (response.status_code == 400 and
                response.json()["success"] is False and
                response.json()["message"] == "Ingredient ids must be provided"), ('Невозможно создать заказ без '
                                                                                   'ингредиентов!')

    @allure.title('Проверка создания заказа с неверным хэшем ингредиентов')
    def test_create_order_with_incorrect_ingredients(self):
        access_token = None
        first_incorrect_ingredient = Helpers().get_random_existing_ingredient()[0] + 'mistake'
        second_incorrect_ingredient = Helpers().get_random_existing_ingredient()[0] + 'mistake'
        with allure.step("Сделать заказ с неверным хэшем ингредиентов"):
            response = OrderApi().create_order([first_incorrect_ingredient, second_incorrect_ingredient], access_token)
        assert (response.status_code == 500 and
                "Internal Server Error" in response.text), 'Невозможно создать заказ при неверном хэше ингредиентов!'
