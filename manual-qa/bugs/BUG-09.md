# BUG-09. Редактирование equipment создаёт дубликат вместо обновления

| Поле | Значение |
|---|---|
| Severity | High (целостность данных) |
| Priority | High |
| Статус | Open |
| Метод подтверждения | Анализ кода: `lib/features/owner/screens/manage_equipment_screen.dart:93-99`; `lib/features/owner/screens/add_equipment_screen.dart:92-101`; `lib/data/providers/owner_equipment_provider.dart:43-52` |
| Тест-кейс | TC-OWN-04 |

## Шаги воспроизведения (UI)

1. Владелец → «Моё оборудование» → редактировать карточку.
2. Изменить название → «Сохранить».

## Фактический результат

Создаётся новый документ с новым ID; старый остаётся. В каталоге два дубля. SnackBar говорит «Оборудование успешно добавлено».

## Ожидаемый результат

Обновляется существующий документ, дублей нет.

## Доказательство в коде

`widget.equipment` используется только для предзаполнения полей в `initState`. В `_saveEquipment()` всегда вызывается `equipmentService.createEquipment(equipmentData, user.uid)`, путь обновления (`updateEquipment`) не используется.

## Влияние

Засорение базы дублями, неверная статистика и поиск.

## Рекомендация

Если `widget.equipment != null`, вызывать update по `widget.equipment.id`; разделить сценарии «создать» и «редактировать».
