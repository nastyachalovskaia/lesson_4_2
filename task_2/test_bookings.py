from constants import BASE_URL


class TestBookings:

    def test_create_booking(self, booking_data, auth_session, create_booking, delete_booking):
        booking_id = create_booking

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Ошибка при получении данных бронирования"

        booking_data_response = get_booking.json()
        assert booking_data_response['firstname'] == booking_data['firstname'], "Имя не совпадает с заданным"
        assert booking_data_response['lastname'] == booking_data['lastname'], "Фамилия не совпадает с заданной"
        assert booking_data_response['totalprice'] == booking_data['totalprice'], "Цена не совпадает с заданной"
        assert booking_data_response['depositpaid'] == booking_data['depositpaid'], "Статус депозита не совпадает"
        assert booking_data_response['bookingdates']['checkin'] == booking_data['bookingdates'][
            'checkin'], "Дата заезда не совпадает"
        assert booking_data_response['bookingdates']['checkout'] == booking_data['bookingdates'][
            'checkout'], "Дата выезда не совпадает"

        delete_booking(booking_id)

        get_deleted_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_deleted_booking.status_code == 404, "Букинг не был удален"

    def test_put_update_booking(self, booking_data, auth_session, create_booking):
        booking_id = create_booking

        updated_booking_data = booking_data.copy()
        updated_booking_data.update({
            "firstname": "Mrs",
            "lastname": "Pimple",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-01-01",
                "checkout": "2025-01-01"
            }
        })

        update_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=updated_booking_data)
        assert update_booking.status_code == 200, "Ошибка при обновлении бронирования"

        get_updated_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_updated_booking.status_code == 200, "Ошибка при получении обновлённых данных бронирования"

        updated_booking_data = get_updated_booking.json()
        assert updated_booking_data['firstname'] == "Mrs", "Имя не обновилось"
        assert updated_booking_data['lastname'] == "Pimple", "Фамилия не обновилась"
        assert updated_booking_data['totalprice'] == 100, "Цена не обновилась"
        assert updated_booking_data['depositpaid'] == True, "Статус депозита не обновился"
        assert updated_booking_data['bookingdates']['checkin'] == "2024-01-01", "Дата регистрации не обновилась"
        assert updated_booking_data['bookingdates']['checkout'] == "2025-01-01", "Дата выезда не обновилась"

    def test_patch_update_booking(self, booking_data, auth_session, create_booking):
        booking_id = create_booking

        updated_booking_data = booking_data.copy()
        updated_booking_data.update({
            "firstname": "Mrs",
            "lastname": "Pimple"
        })

        update_booking = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=updated_booking_data)
        assert update_booking.status_code == 200, "Ошибка при обновлении бронирования"

        get_updated_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_updated_booking.status_code == 200, "Ошибка при получении обновлённых данных бронирования"

        updated_booking_data = get_updated_booking.json()
        assert updated_booking_data['firstname'] == "Mrs", "Имя не обновилось"
        assert updated_booking_data['lastname'] == "Pimple", "Фамилия не обновилась"

        assert updated_booking_data['totalprice'] == booking_data['totalprice'], "Цена изменилась (не должна была)"
        assert updated_booking_data['depositpaid'] == booking_data['depositpaid'], "Статус депозита изменился"
        assert updated_booking_data['bookingdates']['checkin'] == booking_data['bookingdates'][
            'checkin'], "Дата заезда изменилась"
        assert updated_booking_data['bookingdates']['checkout'] == booking_data['bookingdates'][
            'checkout'], "Дата выезда изменилась"

    def test_get_booking_ids(self, booking_data, auth_session, create_booking):

        get_booking = auth_session.get(f"{BASE_URL}/booking")
        assert get_booking.status_code == 200, "Ошибка при получении бронирований"

        booking_ids = get_booking.json()
        assert isinstance(booking_ids, list), "Ответ должен быть списком"

        assert len(booking_ids) > 0, "Список ID бронирований пуст"
