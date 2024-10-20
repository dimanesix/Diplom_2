import allure
import pytest
from faker import Faker

from api.user import UserApi


class TestChangeUserData:
    @allure.title('Проверка изменения данных пользователя с авторизацией')
    @pytest.mark.parametrize('test_field', ["email", "password", "name"])
    @pytest.mark.parametrize('register_user', [(Faker().free_email(), Faker().password(), Faker().first_name())],
                             indirect=True)
    def test_change_user_data_with_auth(self, register_user, test_field):
        _, email, password, name = register_user
        access_token = _.json()["accessToken"]
        if test_field == "email":
            new_email = Faker().free_email()
            with allure.step(f"Обновить поле {test_field} пользователя"):
                response = UserApi().change_user_data(new_email, password, name, access_token)
            assert (response.status_code == 200 and
                    response.json()["success"] is True and
                    response.json()["user"]["email"] == new_email and
                    response.json()["user"][
                        "name"] == name), f'Невозможно обновить данные в поле {test_field} пользователя'
        elif test_field == "password":
            new_password = Faker().password()
            with allure.step(f"Обновить поле {test_field} пользователя"):
                response = UserApi().change_user_data(email, new_password, name, access_token)
            assert (response.status_code == 200 and
                    response.json()["success"] is True and
                    response.json()["user"]["email"] == email and
                    response.json()["user"][
                        "name"] == name), f'Невозможно обновить данные в поле {test_field} пользователя'
        elif test_field == "name":
            new_name = Faker().first_name()
            with allure.step(f"Обновить поле {test_field} пользователя"):
                response = UserApi().change_user_data(email, password, new_name, access_token)
            assert (response.status_code == 200 and
                    response.json()["success"] is True and
                    response.json()["user"]["email"] == email and
                    response.json()["user"][
                        "name"] == new_name), f'Невозможно обновить данные в поле {test_field} пользователя'

    @allure.title('Проверка изменения данных пользователя без авторизации')
    @pytest.mark.parametrize('test_field', ["email", "password", "name"])
    @pytest.mark.parametrize('register_user', [(Faker().free_email(), Faker().password(), Faker().first_name())],
                             indirect=True)
    def test_change_user_data_without_auth(self, register_user, test_field):
        _, email, password, name = register_user
        access_token = None
        if test_field == "email":
            new_email = Faker().free_email()
            with allure.step(f"Обновить поле {test_field} пользователя"):
                response = UserApi().change_user_data(new_email, password, name, access_token)
            assert (response.status_code == 401 and
                    response.json()["success"] is False and
                    response.json()["message"] == "You should be authorised"), (f'Необходимо авторизоваться, чтобы '
                                                                                f'изменить данные в поле {test_field}'
                                                                                f' пользователя')
        elif test_field == "password":
            new_password = Faker().password()
            with allure.step(f"Обновить поле {test_field} пользователя"):
                response = UserApi().change_user_data(email, new_password, name, access_token)
            assert (response.status_code == 401 and
                    response.json()["success"] is False and
                    response.json()["message"] == "You should be authorised"), (f'Необходимо авторизоваться, чтобы '
                                                                                f'изменить данные в поле {test_field}'
                                                                                f' пользователя')
        elif test_field == "name":
            new_name = Faker().first_name()
            with allure.step(f"Обновить поле {test_field} пользователя"):
                response = UserApi().change_user_data(email, password, new_name, access_token)
            assert (response.status_code == 401 and
                    response.json()["success"] is False and
                    response.json()["message"] == "You should be authorised"), (f'Необходимо авторизоваться, чтобы '
                                                                                f'изменить данные в поле {test_field}'
                                                                                f' пользователя')
