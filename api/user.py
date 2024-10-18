import requests
import test_data


class UserApi:
    def register_user(self, email, password, name):
        data = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(url=test_data.REGISTER_USER_ENDPOINT, json=data)
        return response

    def login_user(self, email, password):
        data = {
            "email": email,
            "password": password
        }
        response = requests.post(url=test_data.LOGIN_USER_ENDPOINT, json=data)
        return response

    def change_user_data(self, email, password, name, access_token):
        data = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.patch(url=test_data.USER_DATA_ENDPOINT, json=data, headers={"Authorization": access_token})
        return response

    # def login_user(self, login, password):
    #     data = {
    #         "login": login,
    #         "password": password
    #     }
    #     response = requests.post(test_data.COURIER_ENDPOINT + '/login', json=data)
    #     return response
    #
    #
    # def get_courier_id(self, login, password):
    #     id = self.login_courier(login, password).json()["id"]
    #     return id
    #
    #
    def delete_user(self, access_token):
        requests.delete(url=test_data.USER_DATA_ENDPOINT, headers={"Authorization": f"{access_token}"})

