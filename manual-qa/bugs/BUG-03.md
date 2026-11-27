# BUG-03. Календарь блокирует весь день из-за одного часа брони

| Поле | Значение |
|---|---|
| Severity | Medium (High для UX бронирования) |
| Priority | High |
| Статус | Open |
| Метод подтверждения | Анализ кода: `lib/data/services/booking_service.dart:155-159`; `lib/features/booking/screens/booking_screen.dart:60-65` |
| Тест-кейс | TC-BKG-04 |

## Шаги воспроизведения (UI)

1. Создать бронь 10:00–11:00.
2. Открыть экран бронирования этой же вещи.
3. Попробовать выбрать 15:00 того же дня.

## Фактический результат

День полностью недоступен: `selectableDayPredicate` сравнивает только год/месяц/день, игнорируя время.

## Ожидаемый результат

Доступны все интервалы дня, кроме 10:00–11:00.

## Доказательство в коде

```dart
for (var date = startDate; date.isBefore(endDate);
     date = date.add(const Duration(hours: 1))) {
  bookedDates.add(date);
}
// ...
selectableDayPredicate: (DateTime day) {
  return !_bookedDates.any((bookedDate) =>
      day.year == bookedDate.year &&
      day.month == bookedDate.month &&
      day.day == bookedDate.day);
},
```

## Влияние

Клиент не может забронировать свободное время в тот же день — потеря выручки и плохой UX.

## Рекомендация

Проверять пересечение интервалов (start/end), а не факт брони «в этом дне».
