import allure
import pytest
from faker import Faker
from api.user import UserApi
from helpers import Helpers

# import helpers
import test_data
from api import user


@pytest.fixture
def register_user(request):
    with allure.step('Зарегистрировать пользователя'):
        email, password, name = request.param
        response = UserApi().register_user(email, password, name)
        yield response, email, password, name
        with allure.step('Удалить зарегистрированного пользователя'):
            if response.status_code == 200:
                UserApi().delete_user(response.json()["accessToken"])


@pytest.fixture
def delete_user(request):
    # yield
    with allure.step('Удалить пользователя'):
        UserApi().delete_user(request)
# @pytest.fixture
# def create_courier():
#     with allure.step('Создать курьера'):
#         result = helpers.Helpers().register_new_courier_and_return_login_password_response()
#     return result
#
#
# @pytest.fixture
# def delete_courier(create_courier):
#     yield
#     #   [0] - login, [1] - password
#     with allure.step('Удалить созданного курьера'):
#         id = courier.CourierApi().get_courier_id(create_courier["courier"][0], create_courier["courier"][1])
#         courier.CourierApi().delete_courier(id)
#
#
# @pytest.fixture
# def create_login():
#     with allure.step('Сгенерировать логин'):
#         login = helpers.Helpers().generate_random_string(10)
#     yield login
#     with allure.step('Удалить созданного курьера'):
#         id = courier.CourierApi().get_courier_id(login, test_data.TEST_PASSWORD)
#         courier.CourierApi().delete_courier(id)
