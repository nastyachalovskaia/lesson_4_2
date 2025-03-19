from task_3.constants import BASE_URL
import requests

class TestAuth:
    def test_auth_session(self, auth_session):
        response = auth_session.get(f"{BASE_URL}/api/v1/users/me")
        assert response.status_code == 200, "Ошибка при получении данных пользователя"
        user_data = response.json()
        assert "email" in user_data, "Поле 'email' отсутствует в ответе"

    def test_token(self, get_auth_token):
        token = get_auth_token
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(f"{BASE_URL}/api/v1/users/me", headers=headers)
        assert response.status_code == 200, "Ошибка при получении token"

        test_token_response = requests.post(f"{BASE_URL}/api/v1/login/test-token", headers=headers)
        assert test_token_response.status_code == 200, "Ошибка при test token"

    def test_incorrect_token(self):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "incorrect_token"
        }
        response = requests.get(f"{BASE_URL}/api/v1/users/me", headers=headers)
        assert response.status_code == 401, "Ожидалась ошибка 401 при передаче неверного токена"

    def test_incorrect_credentials(self):
        auth_data = {
            "username": "incorrect_email",
            "password": "incorrect_password"
        }
        response = requests.post(f"{BASE_URL}/api/v1/login/access-token", data=auth_data)
        assert response.status_code == 400, "Ожидалась ошибка 400 при вводе неверных кредов"

    def test_incorrect_method(self):

        auth_data = {
            "username": "incorrect_email",
            "password": "incorrect_password"
        }
        response = requests.get(f"{BASE_URL}/api/v1/login/access-token", data=auth_data)
        assert response.status_code == 405, "Ожидалась ошибка 405 при вводе неверного метода (get вместо post)"



