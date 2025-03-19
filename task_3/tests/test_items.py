import requests
from faker import Faker
from task_3.constants import BASE_URL

fake = Faker()


class TestItems:
    def test_get_items(self, get_items):

        items = get_items
        assert isinstance(items["data"], list), "Ответ должен быть списком"
        assert len(items["data"]) > 0, "Список items не должен быть пустым"

    def test_create_item(self, headers_data):
        headers = headers_data
        data = {
            "title": fake.text(),
            "description":  fake.text()
        }

        response = requests.post(f"{BASE_URL}/api/v1/items/", json=data, headers=headers)
        assert response.status_code == 200, "Не удалось создать item"

        incorrect_data = requests.post(f"{BASE_URL}/api/v1/items/", json={"title": 123, "description": 123}, headers=headers)
        assert incorrect_data.status_code == 422, "Ожидался код 422 в связи с некорректными данными"

    def test_get_item_by_id(self, headers_data, get_items):
        headers = headers_data
        items = get_items
        items_list = items.get("data")
        item_id = items_list[0]["id"]
        assert item_id is not None, "ID item не найден в ответе"

        get_item_by_id = requests.get(f"{BASE_URL}/booking/{item_id}")
        assert get_item_by_id is not None, "ID item не найден в ответе"

        item_id = requests.get(f"{BASE_URL}/api/v1/items/4c6073b8", headers=headers)
        assert item_id.status_code == 422, "ID item must  be Guid"

    def test_item_update(self, headers_data, get_items):

        data = {
            "title": fake.text(),
            "description": fake.text()
        }

        headers = headers_data
        items = get_items
        items_list = items.get("data")
        item_id = items_list[0]["id"]
        assert item_id is not None, "ID item не найден в ответе"

        get_item_by_id = requests.get(f"{BASE_URL}/booking/{item_id}")
        assert get_item_by_id is not None, "ID item не найден в ответе"

        response = requests.put(f"{BASE_URL}/api/v1/items/{item_id}", json=data, headers=headers)
        assert response.status_code == 200, "Ошибка обновления item по id"

        incorrect_data = requests.put(f"{BASE_URL}/api/v1/items/{item_id}", json={"title": 123, "description": 123}, headers=headers)
        assert incorrect_data.status_code == 422, "Ожидался код 422 в связи с некорректными данными для обновления item по id"

    def test_delete_item_by_id(self, headers_data, get_items):
        headers = headers_data
        items = get_items
        items_list = items.get("data")
        item_id = items_list[0]["id"]
        assert item_id is not None, "ID item не найден в ответе"

        get_item_by_id = requests.get(f"{BASE_URL}/booking/{item_id}")
        assert get_item_by_id is not None, "ID item не найден в ответе"

        response = requests.delete(f"{BASE_URL}/api/v1/items/{item_id}", headers=headers)
        assert response.status_code == 200, "Ошибка удаления item по id"









