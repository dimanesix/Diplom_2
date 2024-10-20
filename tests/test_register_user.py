import allure
import pytest
from faker import Faker

import test_data
from api.user import UserApi


class TestRegisterUser:
    @allure.title('Проверка регистрации уникального пользователя')
    @pytest.mark.parametrize('register_user', [(Faker().free_email(), Faker().password(), Faker().first_name())],
                             indirect=True)
    def test_register_unique_user(self, register_user):
        response, email, password, name = register_user
        assert (response.status_code == 200 and
                response.json()["success"] is True and
                "Bearer" in response.json()["accessToken"] and
                response.json()["refreshToken"] is not None and isinstance(response.json()["refreshToken"], str) and
                response.json()["user"]["email"] == email and
                response.json()["user"]["name"] == name), 'Невозможно создать уникального пользователя!'

    @allure.title('Проверка повторной регистрации пользователя')
    @pytest.mark.parametrize('register_user', [(Faker().free_email(), Faker().password(), Faker().first_name())],
                             indirect=True)
    def test_already_register_user(self, register_user):
        response, email, password, name = register_user
        with allure.step("Повторно зарегистрировать пользователя!"):
            response = UserApi().register_user(email, password, name)
        assert (response.status_code == 403 and
                response.json()["success"] is False and response.json()["message"] == "User already exists"), ('Нельзя '
                                                                                                               'повторно зарегистрировать пользователя!')

    @allure.title('Проверка регистрации пользователя без одного из обязательных полей')
    @pytest.mark.parametrize('register_user', [(None, test_data.TEST_PASSWORD, test_data.TEST_NAME),
                                               (test_data.TEST_EMAIL, None, test_data.TEST_NAME),
                                               (test_data.TEST_EMAIL, test_data.TEST_PASSWORD, None)],
                             indirect=True)
    def test_register_user_without_required_field(self, register_user):
        response, email, password, name = register_user
        assert (response.status_code == 403 and
                response.json()["success"] is False and response.json()["message"] == "Email, password and name are "
                                                                                      "required fields"), ('Нельзя '
                                                                                                            'зарегистрировать пользователя без обязательного поля!')