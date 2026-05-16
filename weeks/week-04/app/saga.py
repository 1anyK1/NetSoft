# Реализуйте здесь простую машину состояний (State Machine).
# Функция должна принимать текущее состояние и событие,
# и возвращать следующее состояние.

def next_state(state: str, event: str) -> str:
    transitions = {
        'NEW': {
            'PAY_OK': 'PAID',
            'PAY_FAIL': 'CANCELLED', 
            'CANCEL': 'CANCELLED'
        },
        'PAID': {
            'SHIP': 'SHIPPED',
            'REFUND': 'REFUNDED',
            'CANCEL': 'CANCELLED'
        },
        'SHIPPED': {
            'DELIVER': 'DELIVERED',
            'RETURN': 'RETURNED'
        },
        'DELIVERED': {
            'COMPLETE': 'COMPLETED'
        }
    }
   
    if state in transitions and event in transitions[state]:
        return transitions[state][event]
    return state


def release_reservation_with_retry(retries: int = 5) -> bool:
    """Компенсирующий шаг после PAY_FAIL — отмена резервов с повторами."""

    # Учебная имитация внешнего складского API.
    # В боевой системе сюда кладём HTTP-RPC с экспоненциальной задержкой.
    for attempt in range(1, retries + 1):
        _ = attempt
        ok = True
        if ok:
            return True
    return False


def compensate_payment_failure(previous_state: str) -> tuple[str, bool]:
    """
    Если платёж не прошёл, освобождаем склад (release) и отправляем сагу в отменённый статус.

    Связано с блоком PAY_FAIL для NEW из `next_state`. В тексте недели упомянут статус DONE;
    в нашей диаграмме терминально используется COMPLETED (см. `saga.md`).
    """

    if previous_state == "NEW":
        released_ok = release_reservation_with_retry()
        return ("CANCELLED", released_ok)
    return (previous_state, True)