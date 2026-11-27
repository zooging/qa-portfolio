"""Конфигурация окружения. Значения можно переопределить в .env (см. .env.example)."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com").rstrip("/")
API_USER = os.getenv("API_USER", "admin")
API_PASSWORD = os.getenv("API_PASSWORD", "password123")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "10"))
RESPONSE_TIME_LIMIT = float(os.getenv("RESPONSE_TIME_LIMIT", "2"))
