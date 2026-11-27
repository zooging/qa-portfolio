"""CRUD-сценарии для бронирований."""

from datetime import date, timedelta

import pytest

from client import BookerClient
from data.factories import make_booking_payload


@pytest.mark.regression
def test_create_booking_with_full_payload(created_booking, booking_payload: dict) -> None:
    booking_id, _ = created_booking(booking_payload)

    assert isinstance(booking_id, int) and booking_id > 0


@pytest.mark.regression
def test_create_booking_echoes_all_fields(api: BookerClient, created_booking, booking_payload: dict) -> None:
    booking_id, _ = created_booking(booking_payload)

    body = api.get_booking(booking_id).json()
    assert body == booking_payload


@pytest.mark.regression
def test_create_booking_without_optional_field(created_booking) -> None:
    payload = {key: value for key, value in make_booking_payload().items() if key != "additionalneeds"}

    booking_id, _ = created_booking(payload)

    assert booking_id > 0


@pytest.mark.regression
def test_get_booking_by_id(api: BookerClient, created_booking, booking_payload: dict) -> None:
    booking_id, _ = created_booking(booking_payload)

    response = api.get_booking(booking_id)

    assert response.status_code == 200
    assert response.json()["firstname"] == booking_payload["firstname"]


@pytest.mark.regression
def test_full_update_via_put(api: BookerClient, token: str, created_booking) -> None:
    booking_id, _ = created_booking()
    updated = make_booking_payload(firstname="UpdatedQA", totalprice=555)

    response = api.update_booking(booking_id, updated, token)

    assert response.status_code == 200
    assert api.get_booking(booking_id).json()["firstname"] == "UpdatedQA"


@pytest.mark.regression
def test_partial_update_via_patch(api: BookerClient, token: str, created_booking) -> None:
    booking_id, original = created_booking()

    response = api.patch_booking(booking_id, {"additionalneeds": "Dinner"}, token)

    assert response.status_code == 200
    body = api.get_booking(booking_id).json()
    assert body["additionalneeds"] == "Dinner"
    assert body["firstname"] == original["firstname"]
    assert body["totalprice"] == original["totalprice"]


@pytest.mark.regression
def test_delete_booking(api: BookerClient, token: str, created_booking) -> None:
    booking_id, _ = created_booking()

    response = api.delete_booking(booking_id, token)

    assert response.status_code == 201
    assert api.get_booking(booking_id).status_code == 404


@pytest.mark.negative
def test_delete_already_deleted_booking(api: BookerClient, token: str, created_booking) -> None:
    booking_id, _ = created_booking()
    api.delete_booking(booking_id, token)

    response = api.delete_booking(booking_id, token)

    # Фактическое поведение API: 405 Method Not Allowed, а не 404 Not Found (BUG-006).
    assert response.status_code == 405


@pytest.mark.negative
def test_get_nonexistent_booking(api: BookerClient) -> None:
    response = api.get_booking(99999999)

    assert response.status_code == 404


@pytest.mark.bug
@pytest.mark.xfail(reason="BUG-006: обновление несуществующего бронирования даёт 405 вместо 404", strict=True)
def test_put_nonexistent_booking_returns_404(api: BookerClient, token: str) -> None:
    response = api.update_booking(99999999, make_booking_payload(), token)

    assert response.status_code == 404


@pytest.mark.regression
def test_created_booking_present_in_list(api: BookerClient, created_booking) -> None:
    booking_id, _ = created_booking()

    ids = [item["bookingid"] for item in api.get_bookings().json()]

    assert booking_id in ids


@pytest.mark.regression
def test_created_bookings_have_unique_ids(created_booking) -> None:
    first_id, _ = created_booking()
    second_id, _ = created_booking()

    assert first_id != second_id


@pytest.mark.regression
def test_booking_with_future_dates(created_booking) -> None:
    checkin = (date.today() + timedelta(days=365)).isoformat()
    checkout = (date.today() + timedelta(days=370)).isoformat()

    booking_id, payload = created_booking(
        make_booking_payload(bookingdates={"checkin": checkin, "checkout": checkout})
    )

    assert booking_id > 0
    assert payload["bookingdates"]["checkin"] == checkin


@pytest.mark.negative
def test_put_without_token_forbidden(api: BookerClient, created_booking) -> None:
    booking_id, _ = created_booking()

    response = api.update_booking(booking_id, make_booking_payload())

    assert response.status_code == 403


@pytest.mark.negative
def test_patch_without_token_forbidden(api: BookerClient, created_booking) -> None:
    booking_id, _ = created_booking()

    response = api.patch_booking(booking_id, {"additionalneeds": "Lunch"})

    assert response.status_code == 403


@pytest.mark.negative
def test_delete_without_token_forbidden(api: BookerClient, created_booking) -> None:
    booking_id, _ = created_booking()

    response = api.delete_booking(booking_id)

    assert response.status_code == 403
