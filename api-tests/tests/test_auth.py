"""Авторизация: позитив, негатив и проверка токена на запись."""

import pytest

import config
from client import BookerClient


@pytest.mark.regression
def test_auth_valid_returns_token(api: BookerClient) -> None:
    response = api.auth(config.API_USER, config.API_PASSWORD)

    assert response.status_code == 200
    assert response.json()["token"]


@pytest.mark.regression
def test_auth_token_is_non_empty_string(api: BookerClient) -> None:
    response = api.auth(config.API_USER, config.API_PASSWORD)

    token = response.json()["token"]
    assert isinstance(token, str)
    assert len(token) > 8


@pytest.mark.regression
def test_token_allows_delete(api: BookerClient, token: str, created_booking) -> None:
    booking_id, _ = created_booking()

    response = api.delete_booking(booking_id, token)

    assert response.status_code == 201


@pytest.mark.bug
@pytest.mark.xfail(reason="BUG-005: неверный пароль возвращает 200 вместо 401", strict=True)
def test_wrong_password_returns_401(api: BookerClient) -> None:
    response = api.auth(config.API_USER, "definitely-wrong-password")

    assert response.status_code == 401


@pytest.mark.bug
@pytest.mark.xfail(reason="BUG-005: неизвестный пользователь возвращает 200 вместо 401", strict=True)
def test_unknown_user_returns_401(api: BookerClient) -> None:
    response = api.auth("no-such-user-qa", config.API_PASSWORD)

    assert response.status_code == 401


@pytest.mark.bug
@pytest.mark.xfail(reason="BUG-005: пустой пароль возвращает 200 вместо 401", strict=True)
def test_empty_password_returns_401(api: BookerClient) -> None:
    response = api.auth(config.API_USER, "")

    assert response.status_code == 401


@pytest.mark.negative
def test_invalid_credentials_return_reason_without_token(api: BookerClient) -> None:
    response = api.auth(config.API_USER, "wrong")

    body = response.json()
    assert "token" not in body
    assert body.get("reason") == "Bad credentials"


@pytest.mark.performance
def test_auth_response_time(api: BookerClient) -> None:
    response = api.auth(config.API_USER, config.API_PASSWORD)

    assert response.elapsed.total_seconds() < config.RESPONSE_TIME_LIMIT
