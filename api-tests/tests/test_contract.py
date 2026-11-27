"""Сверка ответов API с JSON-схемами (контрактное тестирование)."""

import json
from pathlib import Path

import pytest
from jsonschema import validate

import config
from client import BookerClient
from data.factories import make_booking_payload

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"


def schema(name: str) -> dict:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


@pytest.mark.contract
def test_get_booking_matches_schema(api: BookerClient, created_booking) -> None:
    booking_id, _ = created_booking()

    validate(api.get_booking(booking_id).json(), schema("booking.json"))


@pytest.mark.contract
def test_create_booking_response_matches_schema(create_response) -> None:
    response = create_response()

    assert response.status_code == 200
    validate(response.json(), schema("booking_create_response.json"))


@pytest.mark.contract
def test_auth_response_matches_schema(api: BookerClient) -> None:
    response = api.auth(config.API_USER, config.API_PASSWORD)

    validate(response.json(), schema("auth_response.json"))


@pytest.mark.contract
def test_booking_list_matches_schema(api: BookerClient) -> None:
    validate(api.get_bookings().json(), schema("booking_list.json"))


@pytest.mark.contract
def test_update_response_matches_schema(api: BookerClient, token: str, created_booking) -> None:
    booking_id, _ = created_booking()

    response = api.update_booking(booking_id, make_booking_payload(), token)

    assert response.status_code == 200
    validate(response.json(), schema("booking.json"))
