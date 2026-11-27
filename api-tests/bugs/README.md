# Баг-репорты

Дефекты найдены при тестировании публичного стенда Restful Booker (`https://restful-booker.herokuapp.com`) 27.11.2026.

| ID | Кратко | Severity | Priority | Статус |
|---|---|---|---|---|
| [BUG-001](BUG-001.md) | 500 при отсутствии обязательных полей | Major | High | Open |
| [BUG-002](BUG-002.md) | checkin позже checkout принимается | Major | High | Open |
| [BUG-003](BUG-003.md) | Строка вместо totalprice → null | Major | Medium | Open |
| [BUG-004](BUG-004.md) | Отрицательная totalprice принимается | Minor | Medium | Open |
| [BUG-005](BUG-005.md) | Неверные креды → 200 вместо 401 | Major | High | Open |
| [BUG-006](BUG-006.md) | 405 вместо 404 для несуществующего ID | Minor | Low | Open |
| [BUG-007](BUG-007.md) | Фильтр checkin не работает | Major | High | Open |
| [BUG-008](BUG-008.md) | Фильтр checkout игнорируется | Major | High | Open |
| [BUG-009](BUG-009.md) | 500 на невалидную дату в фильтре | Minor | Low | Open |

Все дефекты зафиксированы автотестами с маркером `xfail(strict=True)`: после исправления API тест станет XPASS и упадёт — баг пора закрывать.
