import allure
import pytest

from api.user import UserApi


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
