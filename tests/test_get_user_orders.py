import allure
import pytest
from faker import Faker

from api.order import OrderApi
from helpers import Helpers


class TestGetUserOrders:
    @allure.title('Проверка получения заказов авторизованного пользователя')
    @pytest.mark.parametrize('register_user', [(Faker().free_email(), Faker().password(), Faker().first_name())],
                             indirect=True)
    def test_get_user_orders_with_auth(self, register_user):
        _ = register_user[0]
        access_token = _.json()["accessToken"]
        first_order_ingredient = Helpers().get_random_existing_ingredient()
        second_order_ingredient = Helpers().get_random_existing_ingredient()
        with allure.step("Сделать 2 заказа от авторизованного пользователя"):
            OrderApi().create_order([first_order_ingredient[0]], access_token)
            OrderApi().create_order([second_order_ingredient[0]], access_token)
        with allure.step("Получить заказы пользователя"):
            response = OrderApi().get_orders(access_token)
        assert (response.status_code == 200 and
                response.json()["success"] is True and
                # первый заказ
                isinstance(response.json()["orders"][0]["_id"], str) and
                response.json()["orders"][0]["ingredients"][0] == first_order_ingredient[0] and
                response.json()["orders"][0]["status"] == "done" and
                isinstance(response.json()["orders"][0]["createdAt"], str) and
                isinstance(response.json()["orders"][0]["updatedAt"], str) and
                isinstance(response.json()["orders"][0]["number"], int) and
                # второй заказ
                isinstance(response.json()["orders"][1]["_id"], str) and
                response.json()["orders"][1]["ingredients"][0] == second_order_ingredient[0] and
                response.json()["orders"][1]["status"] == "done" and
                isinstance(response.json()["orders"][1]["createdAt"], str) and
                isinstance(response.json()["orders"][1]["updatedAt"], str) and
                isinstance(response.json()["orders"][1]["number"], int) and
                isinstance(response.json()["total"], int) and
                isinstance(response.json()["totalToday"], int)), ('Ошибка при попытке получить заказы авторизованного '
                                                                  'пользователя')

    @allure.title('Проверка получения заказов пользователя без авторизации')
    def test_get_user_orders_without_auth(self):
        access_token = None
        with allure.step("Попытаться получить заказы пользователя без авторизации"):
            response = OrderApi().get_orders(access_token)
        assert (response.status_code == 401 and
                response.json()["success"] is False and
                response.json()["message"] == "You should be authorised"), ('Невозможно получить заказы пользователя '
                                                                            'без авторизации')
