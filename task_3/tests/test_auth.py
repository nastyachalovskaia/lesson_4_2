from task_3.constants import BASE_URL
import requests

class TestAuth:
    def test_auth_session(self, auth_session):
        response = auth_session.get(f"{BASE_URL}/api/v1/users/me")
        assert response.status_code == 200, "Ошибка при получении данных пользователя"
        user_data = response.json()
        assert "email" in user_data, "Поле 'email' отсутствует в ответе"



