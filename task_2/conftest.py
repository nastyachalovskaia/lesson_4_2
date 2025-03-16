import pytest
import requests
from faker import Faker

from constants import HEADERS, BASE_URL

fake = Faker()

# Генерация простых данных
print(fake.name())
print(fake.address())

@pytest.fixture(scope="session")
def auth_session():
    """Создаёт сессию с авторизацией и возвращает объект сессии."""
    session = requests.Session()
    session.headers.update(HEADERS)

    auth_response = session.post(f"{BASE_URL}/auth", json={"username": "admin", "password": "password123"})
    assert auth_response.status_code == 200, "Ошибка авторизации, статус код не 200"
    token = auth_response.json().get("token")
    assert token is not None, "Токен не найден в ответе"

    session.headers.update({"Cookie": f"token={token}"})
    return session

@pytest.fixture()
def create_booking(auth_session, booking_data):

    create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
    assert create_booking.status_code == 200
    booking_id = create_booking.json().get("bookingid")
    assert booking_id is not None, "ID букинга не найден в ответе"

    return booking_id

@pytest.fixture
def delete_booking(auth_session):
    def _delete_booking(booking_id):
        delete_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert delete_booking.status_code == 201, f"Ошибка при удалении букинга с ID {booking_id}"
    return _delete_booking


@pytest.fixture()
def booking_data():
    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=100, max=10000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Breakfast"
    }
