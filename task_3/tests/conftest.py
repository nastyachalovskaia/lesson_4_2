import pytest
import requests
from task_3.constants import BASE_URL, HEADERS


@pytest.fixture(scope="session")
def auth_session():
    """Создаёт сессию с авторизацией и возвращает объект сессии."""
    session = requests.Session()
    session.headers.update(HEADERS)

    auth_data = {
        "username": "nenjuhajujanic@mail.ru",
        "password": "Qwerty11_33"
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
def create_item_id(auth_session, item_data):
    create_item = auth_session.post(f"{BASE_URL}/items", json=item_data)
    assert create_item.status_code == 200
    item_id = create_item.json().get("itemid")
    assert item_id is not None, "ID не найден в ответе"

    return item_id


@pytest.fixture()
def item_data():
    return {
        "title": "string",
        "description": "string"
    }
