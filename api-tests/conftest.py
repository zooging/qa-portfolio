"""Общие фикстуры: клиент, токен и автоочистка созданных бронирований."""

import warnings

import pytest

import config
from client import BookerClient
from data.factories import make_booking_payload


@pytest.fixture(scope="session")
def api() -> BookerClient:
    return BookerClient(config.BASE_URL)


@pytest.fixture(scope="session")
def token(api: BookerClient) -> str:
    response = api.auth(config.API_USER, config.API_PASSWORD)
    assert response.status_code == 200, response.text
    body = response.json()
    assert "token" in body and body["token"], body
    return body["token"]


@pytest.fixture
def booking_payload() -> dict:
    """Свежий валидный payload для каждого теста."""
    return make_booking_payload()


def _cleanup(api: BookerClient, token: str, ids: list[int]) -> None:
    for booking_id in ids:
        cleanup = api.delete_booking(booking_id, token)
        if cleanup.status_code not in (201, 404, 405):
            warnings.warn(
                f"Не удалось удалить бронирование {booking_id}: "
                f"{cleanup.status_code} {cleanup.text}"
            )


@pytest.fixture
def created_booking(api: BookerClient, token: str):
    """Фабрика бронирований с гарантированной очисткой после теста."""
    created: list[int] = []

    def create(payload: dict | None = None) -> tuple[int, dict]:
        body = payload if payload is not None else make_booking_payload()
        response = api.create_booking(body)
        assert response.status_code == 200, response.text
        booking_id = response.json()["bookingid"]
        created.append(booking_id)
        return booking_id, body

    yield create

    _cleanup(api, token, created)


@pytest.fixture
def create_response(api: BookerClient, token: str):
    """Фабрика, возвращающая сам HTTP-ответ POST /booking (нужна для схем)."""
    created: list[int] = []

    def create(payload: dict | None = None):
        response = api.create_booking(payload if payload is not None else make_booking_payload())
        if response.status_code == 200:
            created.append(response.json()["bookingid"])
        return response

    yield create

    _cleanup(api, token, created)
