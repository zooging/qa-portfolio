"""Фильтрация списка бронирований (главный источник находок дефектов)."""

from datetime import date, timedelta

import pytest

from client import BookerClient
from data.factories import make_booking_payload, unique_name


@pytest.mark.regression
def test_filter_by_firstname(api: BookerClient, created_booking) -> None:
    firstname = unique_name()
    booking_id, _ = created_booking(make_booking_payload(firstname=firstname))

    ids = [item["bookingid"] for item in api.get_bookings(firstname=firstname).json()]

    assert ids == [booking_id]


@pytest.mark.regression
def test_filter_by_lastname(api: BookerClient, created_booking) -> None:
    lastname = unique_name()
    booking_id, _ = created_booking(make_booking_payload(lastname=lastname))

    ids = [item["bookingid"] for item in api.get_bookings(lastname=lastname).json()]

    assert booking_id in ids


@pytest.mark.regression
def test_filter_by_firstname_and_lastname(api: BookerClient, created_booking) -> None:
    firstname, lastname = unique_name(), unique_name()
    booking_id, _ = created_booking(
        make_booking_payload(firstname=firstname, lastname=lastname)
    )

    ids = [
        item["bookingid"]
        for item in api.get_bookings(firstname=firstname, lastname=lastname).json()
    ]

    assert ids == [booking_id]


@pytest.mark.bug
@pytest.mark.xfail(reason="BUG-007: фильтр checkin игнорируется и возвращает пустой список", strict=True)
def test_filter_by_checkin(api: BookerClient, created_booking) -> None:
    checkin = (date.today() + timedelta(days=700)).isoformat()
    booking_id, _ = created_booking(
        make_booking_payload(bookingdates={"checkin": checkin, "checkout": (date.today() + timedelta(days=704)).isoformat()})
    )

    ids = [item["bookingid"] for item in api.get_bookings(checkin=checkin).json()]

    assert booking_id in ids


@pytest.mark.bug
@pytest.mark.xfail(reason="BUG-008: фильтр checkout не применяется, возвращаются все бронирования", strict=True)
def test_filter_by_checkout(api: BookerClient, created_booking) -> None:
    checkout = (date.today() + timedelta(days=705)).isoformat()
    booking_id, _ = created_booking(
        make_booking_payload(bookingdates={"checkin": (date.today() + timedelta(days=701)).isoformat(), "checkout": checkout})
    )

    ids = [item["bookingid"] for item in api.get_bookings(checkout=checkout).json()]

    assert len(ids) <= 10 and booking_id in ids


@pytest.mark.bug
@pytest.mark.xfail(reason="BUG-007: фильтр checkin не работает и в связке с checkout", strict=True)
def test_filter_by_checkin_and_checkout(api: BookerClient, created_booking) -> None:
    checkin = (date.today() + timedelta(days=710)).isoformat()
    checkout = (date.today() + timedelta(days=714)).isoformat()
    booking_id, _ = created_booking(
        make_booking_payload(bookingdates={"checkin": checkin, "checkout": checkout})
    )

    ids = [
        item["bookingid"]
        for item in api.get_bookings(checkin=checkin, checkout=checkout).json()
    ]

    assert booking_id in ids


@pytest.mark.regression
def test_filter_unknown_firstname_returns_empty_list(api: BookerClient) -> None:
    response = api.get_bookings(firstname=unique_name())

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.bug
@pytest.mark.xfail(reason="BUG-009: невалидная дата в фильтре даёт 500 вместо 400", strict=True)
def test_filter_invalid_date_returns_400(api: BookerClient) -> None:
    response = api.get_bookings(checkin="not-a-date")

    assert response.status_code == 400
