"""Тонкий HTTP-клиент Restful Booker.

Все запросы идут через один requests.Session — так проще переиспользовать
соединение и задать общие заголовки/таймаут.
"""

from typing import Any

import allure
import requests

import config


class BookerClient:
    def __init__(self, base_url: str = config.BASE_URL) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        kwargs.setdefault("timeout", config.REQUEST_TIMEOUT)
        return self.session.request(method, f"{self.base_url}{path}", **kwargs)

    @allure.step("GET /ping — проверка доступности API")
    def ping(self) -> requests.Response:
        return self._request("GET", "/ping")

    @allure.step("POST /auth — получение токена")
    def auth(self, username: str, password: str) -> requests.Response:
        return self._request(
            "POST", "/auth", json={"username": username, "password": password}
        )

    @allure.step("GET /booking — список бронирований с фильтрами")
    def get_bookings(self, **params: Any) -> requests.Response:
        return self._request("GET", "/booking", params=params or None)

    @allure.step("GET /booking/{booking_id}")
    def get_booking(self, booking_id: int | str) -> requests.Response:
        return self._request("GET", f"/booking/{booking_id}")

    @allure.step("POST /booking — создание бронирования")
    def create_booking(self, payload: dict[str, Any]) -> requests.Response:
        return self._request("POST", "/booking", json=payload)

    @allure.step("PUT /booking/{booking_id} — полное обновление")
    def update_booking(
        self, booking_id: int | str, payload: dict[str, Any], token: str | None = None
    ) -> requests.Response:
        return self._request(
            "PUT", f"/booking/{booking_id}", json=payload, cookies=self._auth_cookie(token)
        )

    @allure.step("PATCH /booking/{booking_id} — частичное обновление")
    def patch_booking(
        self, booking_id: int | str, payload: dict[str, Any], token: str | None = None
    ) -> requests.Response:
        return self._request(
            "PATCH", f"/booking/{booking_id}", json=payload, cookies=self._auth_cookie(token)
        )

    @allure.step("DELETE /booking/{booking_id}")
    def delete_booking(self, booking_id: int | str, token: str | None = None) -> requests.Response:
        return self._request(
            "DELETE", f"/booking/{booking_id}", cookies=self._auth_cookie(token)
        )

    @staticmethod
    def _auth_cookie(token: str | None) -> dict[str, str] | None:
        return {"token": token} if token else None
