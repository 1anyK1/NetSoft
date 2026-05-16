# Saga описание для проекта tickets-s01

## Проект
- **project_code**: tickets-s01
- **Ресурс**: tickets
- **Группа**: 332
- **Студент**: s01

## Описание саги для обработки заказа билетов

### Состояния (States):
- **NEW** - новый заказ создан
- **PAID** - заказ оплачен
- **SHIPPED** - билеты отправлены
- **DELIVERED** - билеты доставлены
- **COMPLETED** - заказ завершен
- **FAILED** - оплата не прошла
- **CANCELLED** - заказ отменен
- **REFUNDED** - возврат средств
- **RETURNED** - билеты возвращены

### События (Events):
- **PAY_OK** - оплата успешна
- **PAY_FAIL** - ошибка оплаты
- **SHIP** - отправка билетов
- **DELIVER** - доставка билетов
- **COMPLETE** - завершение заказа
- **CANCEL** - отмена заказа
- **REFUND** - возврат средств
- **RETURN** - возврат билетов
- **RETRY** - повторная попытка

### Транзишены (Transitions):

## Диаграмма переходов статусов

```mermaid
stateDiagram-v2
    [*] --> NEW: создание заказа
    
    NEW --> PAID: PAY_OK
    NEW --> CANCELLED: PAY_FAIL
    NEW --> CANCELLED: CANCEL
    
    PAID --> SHIPPED: SHIP
    PAID --> REFUNDED: REFUND
    PAID --> CANCELLED: CANCEL
    
    SHIPPED --> DELIVERED: DELIVER
    SHIPPED --> RETURNED: RETURN
    
    DELIVERED --> COMPLETED: COMPLETE
    
    CANCELLED --> [*]
    REFUNDED --> [*]
    RETURNED --> [*]
    COMPLETED --> [*]
    
    note right of NEW: начальное состояние
    note right of COMPLETED: конечное состояние
    note right of CANCELLED: терминальное состояние
    note right of REFUNDED: терминальное состояние
    note right of RETURNED: терминальное состояние