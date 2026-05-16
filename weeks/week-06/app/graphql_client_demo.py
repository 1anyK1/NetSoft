"""
Клиент по README недели 06: отправка Query и Mutation в GraphQL (httpx).

Ожидается поднятый GraphQL-сервер (например, недели 05) под тем же «доменом», что даёт ваша схема.
Порт по умолчанию совпадает с week-05 для items (8101).

Пример:
    export GROUP=332 STUDENT_ID=s01
    GRAPHQL_URL=http://127.0.0.1:8101/graphql python graphql_client_demo.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import httpx

REPO_ROOT = Path(__file__).resolve().parents[3]
APP_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(APP_DIR))

from client import build_payload  # noqa: E402
from coursekit.variant import load_variant  # noqa: E402


def main() -> None:
    os.environ.setdefault("GROUP", "332")
    os.environ.setdefault("STUDENT_ID", "s01")

    url = os.environ.get("GRAPHQL_URL", "http://127.0.0.1:8101/graphql")
    v = load_variant("06")
    g = v["graphql"]

    # Для недели 05 сервер экспонирует items/createItem — для демо используем их,
    # если свой сервер недоступен, вы увидите errors в консоли.
    q_str = """query DemoList {
      items {
        id
        name
        sku
      }
    }"""

    mutation_str = """mutation DemoCreate($input: CreateItemInput!) {
      createItem(input: $input) {
        id
        name
        sku
      }
    }"""

    variables_demo = {"input": {"name": "Demo", "sku": "SKU-06", "price": 1.0, "quantity": 1}}

    with httpx.Client(timeout=30.0) as client:
        for label, payload in (
            ("query", build_payload(q_str, {})),
            ("mutation", build_payload(mutation_str, variables_demo)),
        ):
            r = client.post(url, json=payload)
            body = r.json()
            print(f"[{label}] HTTP {r.status_code} | project `{v['project_code']}` | graphql `{g['type']}`")
            if body.get("errors"):
                print("  errors:", body["errors"])
            if body.get("data") is not None:
                print("  data:", body["data"])


if __name__ == "__main__":
    main()
