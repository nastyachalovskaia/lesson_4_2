import pytest
import requests
from faker import Faker

from task_3.constants import BASE_URL, HEADERS

fake = Faker()


@pytest.fixture(scope="session")
def auth_session():
    """Создаёт сессию с авторизацией и возвращает объект сессии."""
    session = requests.Session()
    session.headers.update(HEADERS)

    auth_data = {
        "username": "email",
        "password": "secret"
    }

    auth_response = session.post(f"{BASE_URL}/api/v1/login/access-token", data=auth_data)
    assert auth_response.status_code == 200, "Ошибка авторизации, статус код не 200"

    access_token = auth_response.json().get("access_token")
    assert access_token is not None, "Токен не найден в ответе"

    session.headers.update({"Authorization": f"Bearer {access_token}"})
    assert "Authorization" in session.headers, "Заголовок Authorization отсутствует"
    assert session.headers["Authorization"] == f"Bearer {access_token}", "Токен в заголовке Authorization некорректен"

    return session

@pytest.fixture()
def get_auth_token():
    auth_data = {
        "username": "email",
        "password": "secret"
    }
    response = requests.post(f"{BASE_URL}/api/v1/login/access-token", data=auth_data)
    assert response.status_code == 200

    return response.json().get("access_token")

@pytest.fixture()
def headers_data(get_auth_token):
    token = get_auth_token
    return  {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

@pytest.fixture()
def get_items(headers_data):
    headers = headers_data

    response = requests.get(f"{BASE_URL}/api/v1/items/", headers=headers)
    assert response.status_code == 200, "Список items не получен"

    items = response.json()
    return items

