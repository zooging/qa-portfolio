# API-автотесты Restful Booker (pytest + requests + Allure + CI)

[![API tests](https://github.com/zooging/qa-portfolio/actions/workflows/api-tests.yml/badge.svg)](https://github.com/zooging/qa-portfolio/actions/workflows/api-tests.yml)
[![Allure report](https://img.shields.io/badge/Allure-report-blue)](https://zooging.github.io/qa-portfolio/)

## Что тестировалось

Публичный API сервиса бронирований [Restful Booker](https://github.com/mwinteringham/restful-booker): `https://restful-booker.herokuapp.com`.

Покрытые сценарии: авторизация, CRUD бронирований, поиск по имени/датам, проверка JSON-схем, негативные и граничные случаи, время отклика.

## Стек

Python 3.11+, pytest 9, requests, jsonschema, allure-pytest, pytest-html, Faker, python-dotenv, GitHub Actions.

## Что сделал

- **52 автотеста**: 35 позитивных/стабильных + 17 сценариев на известные дефекты (`xfail(strict=True)`);
- генерация уникальных тестовых данных через Faker и `uuid4`, автоудаление созданных бронирований в фикстурах;
- ENV-конфиг (`BASE_URL`, креды, таймауты, порог времени отклика) через `.env`;
- проверка контракта: 4 JSON-схемы в `schemas/`;
- **9 баг-репортов** с шагами, ожидаемым/фактическим результатом и ссылкой на тест — см. [`bugs/`](bugs/README.md);
- отчёты Allure (result-файлы + публикация на GitHub Pages) и самодостаточный HTML-отчёт;
- CI: прогон на каждый push/PR и раз в неделю, артефакты отчётов, бейдж в README.

## Результаты последнего локального прогона (27.11.2026)

| Метрика | Значение |
|---|---:|
| Всего сценариев | 52 |
| Passed | 35 |
| Xfailed (подтверждённые дефекты) | 17 |
| Failed | 0 |
| Время прогона | 21,4 с |
| Найдено дефектов | 9 |

> Xfail здесь — не «пропущенный тест», а зафиксированное расхождение с ожидаемым поведением API. Все они описаны в `bugs/` и при исправлении API превратятся в XPASS, что упадёт сборка и сигнализирует: пора обновить баг-репорт.

## Запуск локально

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python -m pytest --alluredir=allure-results --html=report.html --self-contained-html
```

Для просмотра Allure-отчёта локально нужен Allure CLI (Java 17+):

```powershell
allure serve allure-results
```

Без Java можно открыть `report.html` — он самодостаточный.

## Структура

```text
api-tests/
  client.py              # HTTP-клиент с allure.step
  config.py              # конфигурация из .env
  conftest.py            # фикстуры и очистка данных
  data/factories.py      # генерация тестовых данных
  schemas/               # JSON-схемы ответов
  tests/                 # 52 теста по 7 файлам
  bugs/                  # 9 баг-репортов
  .github/workflows/     # CI и публикация Allure
```

## Ссылки

- Все проекты портфолио: https://github.com/zooging/qa-portfolio
- Allure-отчёт: https://zooging.github.io/qa-portfolio/
- Исходный API: https://github.com/mwinteringham/restful-booker
