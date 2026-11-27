"""Простая проверка времени отклика без нагрузочного инструмента."""

import time

import pytest

import config
from client import BookerClient
from data.factories import make_booking_payload


@pytest.mark.performance
def test_get_booking_average_response_time(api: BookerClient, created_booking) -> None:
    booking_id, _ = created_booking()
    timings = []
    for _ in range(5):
        response = api.get_booking(booking_id)
        assert response.status_code == 200
        timings.append(response.elapsed.total_seconds())

    assert sum(timings) / len(timings) < config.RESPONSE_TIME_LIMIT


@pytest.mark.performance
def test_create_booking_response_time(create_response) -> None:
    response = create_response()

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < config.RESPONSE_TIME_LIMIT


@pytest.mark.performance
def test_get_bookings_list_response_time(api: BookerClient) -> None:
    start = time.monotonic()
    response = api.get_bookings()
    elapsed = time.monotonic() - start

    assert response.status_code == 200
    assert elapsed < config.RESPONSE_TIME_LIMIT
