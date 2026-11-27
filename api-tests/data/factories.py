"""Генерация тестовых данных: уникальные имена, корректные и невалидные даты."""

from datetime import date, timedelta
from uuid import uuid4

from faker import Faker

fake = Faker("en_US")


def unique_name() -> str:
    """Уникальный префикс, чтобы фильтры не пересекались с чужими бронированиями."""
    return f"QA{uuid4().hex[:8]}"


def future_dates() -> tuple[str, str]:
    checkin = date.today() + timedelta(days=30)
    checkout = checkin + timedelta(days=4)
    return checkin.isoformat(), checkout.isoformat()


def make_booking_payload(**overrides: object) -> dict[str, object]:
    checkin, checkout = future_dates()
    payload: dict[str, object] = {
        "firstname": unique_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=100, max=9999),
        "depositpaid": True,
        "bookingdates": {"checkin": checkin, "checkout": checkout},
        "additionalneeds": "Breakfast",
    }
    for key, value in overrides.items():
        if key == "bookingdates":
            payload["bookingdates"] = dict(value)  # type: ignore[arg-type]
        else:
            payload[key] = value
    return payload
