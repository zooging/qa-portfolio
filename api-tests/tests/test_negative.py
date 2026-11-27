"""Негативные и граничные сценарии.

Ожидаемое поведение описано в assert; если API исправят, xfail станет XPASS
и тест упадёт — это сигнал обновить баг-репорт и убрать xfail.
"""

import pytest

from client import BookerClient
from data.factories import make_booking_payload


@pytest.mark.bug
@pytest.mark.xfail(reason="BUG-001: пропущенное обязательное поле даёт 500 вместо 400", strict=True)
@pytest.mark.parametrize("field", ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"])
@pytest.mark.negative
def test_create_without_required_field(api: BookerClient, field: str) -> None:
    payload = make_booking_payload()
    payload.pop(field)

    response = api.create_booking(payload)

    assert response.status_code == 400


@pytest.mark.bug
@pytest.mark.xfail(reason="BUG-001: пустое тело даёт 500 вместо 400", strict=True)
@pytest.mark.negative
def test_create_with_empty_body(api: BookerClient) -> None:
    response = api.create_booking({})

    assert response.status_code == 400


@pytest.mark.bug
@pytest.mark.xfail(reason="BUG-002: checkout раньше checkin принимается", strict=True)
@pytest.mark.negative
def test_create_with_reversed_dates(api: BookerClient, token: str) -> None:
    payload = make_booking_payload(
        bookingdates={"checkin": "2027-05-10", "checkout": "2027-05-01"}
    )
    booking_id = None
    try:
        response = api.create_booking(payload)
        if response.status_code == 200:
            booking_id = response.json()["bookingid"]
        assert response.status_code == 400
    finally:
        if booking_id is not None:
            api.delete_booking(booking_id, token)


@pytest.mark.bug
@pytest.mark.xfail(reason="BUG-003: строка вместо цены принимается и превращается в null", strict=True)
@pytest.mark.negative
def test_create_with_string_price(api: BookerClient, token: str) -> None:
    booking_id = None
    try:
        response = api.create_booking(make_booking_payload(totalprice="abc"))
        if response.status_code == 200:
            booking_id = response.json()["bookingid"]
        assert response.status_code == 400
    finally:
        if booking_id is not None:
            api.delete_booking(booking_id, token)


@pytest.mark.bug
@pytest.mark.xfail(reason="BUG-004: отрицательная цена принимается", strict=True)
@pytest.mark.negative
def test_create_with_negative_price(api: BookerClient, token: str) -> None:
    booking_id = None
    try:
        response = api.create_booking(make_booking_payload(totalprice=-5))
        if response.status_code == 200:
            booking_id = response.json()["bookingid"]
        assert response.status_code == 400
    finally:
        if booking_id is not None:
            api.delete_booking(booking_id, token)


@pytest.mark.negative
def test_get_booking_by_non_numeric_id(api: BookerClient) -> None:
    response = api.get_booking("not-an-id")

    assert response.status_code == 404
