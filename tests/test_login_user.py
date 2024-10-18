import allure
import pytest
from faker import Faker

from api.user import UserApi


class TestLoginUser:
    @allure.title('Проверка авторизации пользователя')
    @pytest.mark.parametrize('register_user', [(Faker().free_email(), Faker().password(), Faker().first_name())],
                             indirect=True)
    def test_login_user(self, register_user):
        _, email, password, name = register_user
        with allure.step('Залогиниться пользователем'):
            response = UserApi().login_user(email, password)
        assert (response.status_code == 200 and
                response.json()["success"] is True and
                "Bearer" in response.json()["accessToken"] and
                response.json()["refreshToken"] is not None and isinstance(response.json()["refreshToken"], str) and
                response.json()["user"]["email"] == email and
                response.json()["user"]["name"] == name), 'Невозможно залогиниться пользователем!'

    @allure.title('Проверка авторизации пользователя с ошибкой в логине и пароле')
    @pytest.mark.parametrize('register_user', [(Faker().free_email(), Faker().password(), Faker().first_name())],
                             indirect=True)
    def test_login_user_with_mistakes(self, register_user):
        _, email, password, name = register_user
        with allure.step('Залогиниться пользователем c допущенной ошибкой в логине и пароле'):
            response = UserApi().login_user(email+'mistake', password+'mistake')
        assert (response.status_code == 401 and
                response.json()["success"] is False and response.json()[
                    "message"] == "email or password are incorrect"), 'Невозможно залогиниться пользователем с ошибкой в логине и пароле!'

