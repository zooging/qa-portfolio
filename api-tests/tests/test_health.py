"""Smoke-проверки доступности сервиса."""

import pytest

import config
from client import BookerClient


@pytest.mark.smoke
def test_ping_returns_created(api: BookerClient) -> None:
    response = api.ping()

    assert response.status_code == 201
    assert response.text.strip() == "Created"


@pytest.mark.smoke
@pytest.mark.performance
def test_ping_response_time(api: BookerClient) -> None:
    response = api.ping()

    assert response.elapsed.total_seconds() < config.RESPONSE_TIME_LIMIT
