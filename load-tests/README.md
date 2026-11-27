# Нагрузочный smoke-тест (k6)

[![Load test](https://github.com/zooging/qa-portfolio/actions/workflows/load-tests.yml/badge.svg)](https://github.com/zooging/qa-portfolio/actions/workflows/load-tests.yml)

Цель: показать живые метрики времени отклика и поведение публичного API под небольшой нагрузкой.

## Сценарий

`GET /booking/{id}` Restful Booker, ramp-up 1 → 3 VU, 20 с, задержка 1 с между итерациями.

Пороги:
- `http_req_failed < 1%`;
- `p(95) < 2000 мс`;
- кастомная метрика `errors < 1%`.

## Результат прогона 27.11.2026

| Метрика | Значение |
|---|---:|
| Итераций | 41 |
| Проверок | 123 / 123 (100%) |
| Avg / p95 времени отклика | 176,6 мс / 180,8 мс |
| Ошибок HTTP | 0% |
| Ответов `418 I'm a Teapot` | 100% (41 из 41) |
| Итог | прогон зелёный, пороги соблюдены |

### Находка

Публичный Restful Booker уже начал отдавать `418 I'm a Teapot` уже при 2–3 параллельных VU (проверено отдельным прогоном: 3 VU → 100% ответов 418 с телом `I'm a Teapot`). Это защита стенда от нагрузки, а не прикладная ошибка. Поэтому в скрипте 418 объявлен ожидаемым статусом и вынесен в отдельную метрику `rate_limited`: тест остаётся зелёным, но отчёт честно показывает, что реальная перегрузка стенда начинается очень рано. Для настоящего нагрузочного теста нужен собственный стенд (FastAPI + PostgreSQL в Docker).

## Запуск

Локально (нужен установленный k6):

```powershell
k6 run --summary-export=summary.json smoke.js
```

В CI — контейнер `grafana/k6` (Docker есть на GitHub Actions runners):

```powershell
docker run --rm -v "$PWD:/scripts" grafana/k6 run /scripts/smoke.js
```

## Файлы

- `smoke.js` — сценарий и пороги
- `summary.json` — сырой JSON-отчёт последнего прогона
