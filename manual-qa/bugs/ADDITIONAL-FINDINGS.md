# Дополнительные находки (5)

Подтверждены чтением кода, но не вынесены в отдельные баг-репорты из-за меньшего влияния.

| ID | Файл:строка | Суть | Severity | Связанный тест |
|---|---|---|---|---|
| A1 | `lib/features/equipment/widgets/search_bar.dart:8-20,62-71`; `lib/data/providers/equipment_provider.dart:26,53-56,88-97` | Два разных `sortOptionProvider`: чипы сортировки меняют один, `filteredEquipmentProvider` слушает другой — сортировка в каталоге не работает. Дополнительно `createdAt` не записывается при создании | Medium | TC-CAT-03, TC-CAT-04 |
| A2 | `lib/features/home/screens/home_screen.dart:101-107` | Категории меняют только `_selectedCategoryIndex`; `updateCategory` не вызывается (TODO) — фильтр не работает | Medium | TC-CAT-05 |
| A3 | `lib/features/auth/screens/sign_in_screen.dart:73-86`; `lib/data/services/auth_service.dart:224-245` | Сервис возвращает русскоязычные ошибки, а `_getErrorMessage` ищет англоязычные коды — пользователь видит «Ошибка входа: Неверный пароль» | Low | TC-AUTH-02 |
| A4 | `lib/features/auth/screens/sign_up_screen.dart:112-135` | Email валидируется только по наличию `@`, телефон — только на непустоту (`abc` проходит) | Low | TC-AUTH-03 |
| A5 | `lib/data/services/booking_service.dart:457-461`; `lib/features/rental_history/screens/rental_detail_screen.dart:118-133` | `calculateCancellationFee` возвращает `0.0` при любой ошибке — штраф молча обнуляется в UI | Low/Medium | TC-BKG-06 |
