# E2E-тесты на Playwright (SauceDemo)

[![E2E tests](https://github.com/zooging/qa-portfolio/actions/workflows/e2e-tests.yml/badge.svg)](https://github.com/zooging/qa-portfolio/actions/workflows/e2e-tests.yml)

## Что тестировалось

Публичный демо-магазин [SauceDemo](https://www.saucedemo.com/) — стабильный стенд с логином, каталогом, корзиной и оформлением заказа.

> Почему не OWASP Juice Shop, как в исходном плане: локальный Docker недоступен, а публичные демо-инстансы нестабильны. Для CI важнее воспроизводимость. Те же самые практики (expect-assertions, скриншоты и видео при падении, трассировки, Allure) отработаны полностью.

## Стек

Node.js 20+, Playwright Test, JavaScript, Allure Playwright, GitHub Actions.

## Что сделал

- **15 E2E-сценариев**: логин (включая негатив и locked user), каталог и сортировка, карточка товара, корзина, полный checkout и валидация формы;
- **expect-assertions** вместо ручных `waitForTimeout` — устранены флаки;
- скриншоты и видео при падении, trace при первом retry;
- параллельный запуск (4 воркера локально, 2 в CI), retry только в CI;
- Allure-результаты и HTML-отчёт Playwright;
- CI на каждый push/PR и раз в неделю.

## Результаты последнего локального прогона (27.11.2026)

| Метрика | Значение |
|---|---:|
| Сценариев | 15 |
| Passed | 15 |
| Failed | 0 |
| Время прогона | 7,7 с |
| Браузер | Chromium (Desktop Chrome) |

## Запуск

```powershell
npm install
npx playwright install chromium
npx playwright test
npx playwright show-report
```

Allure-результаты лежат в `allure-results/`; для локального просмотра нужен Allure CLI (Java 17+): `allure serve allure-results`.

## Структура

```text
e2e-playwright/
  playwright.config.js   # baseURL, репортеры, трассировки, воркеры
  tests/
    helpers.js           # логин и добавление товара
    auth.spec.js         # 4 теста
    inventory.spec.js    # 4 теста
    cart.spec.js         # 4 теста
    checkout.spec.js     # 3 теста
```

## Ссылки

- Все проекты портфолио: https://github.com/zooging/qa-portfolio
- Демо-стенд: https://www.saucedemo.com
