# Реализуйте здесь клиент для GraphQL.

PROJECT_CODE = "users-s01"


def build_payload(query: str, variables: dict) -> dict:
    """
    Формирует словарь для отправки GraphQL запроса.

    :param query: Текст запроса (query или mutation).
    :param variables: Словарь с переменными.
    :return: Словарь с ключами "query" и "variables".
    """
    return {"query": query, "variables": variables}
