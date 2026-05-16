"""Дополнительные проверки по условию README недели 02 (локальная самопроверка)."""

import importlib.util
from pathlib import Path

from coursekit.variant import load_variant
from fastapi.testclient import TestClient

WEEK = "02"
ROOT = Path(__file__).resolve().parents[3]
APP_PATH = ROOT / "weeks" / "week-02" / "app" / "main.py"


def _load_app():
    spec = importlib.util.spec_from_file_location("week02_app", APP_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.app


def _extra_sample(t: str):
    return {"str": "x", "int": 1, "float": 2.5, "bool": True}[t]


def test_put_success_returns_updated():
    v = load_variant(WEEK)
    resource = v["resource"]
    extra = v["extra_field"]
    client = TestClient(_load_app())
    r = client.post(
        f"/{resource}",
        json={"name": "A", extra["name"]: _extra_sample(extra["type"])},
    )
    rid = r.json()["id"]
    r2 = client.put(
        f"/{resource}/{rid}",
        json={"name": "B", extra["name"]: _extra_sample(extra["type"])},
    )
    assert r2.status_code == 200
    body = r2.json()
    assert body["name"] == "B"
    assert body["id"] == rid


def test_delete_unknown_returns_404():
    v = load_variant(WEEK)
    resource = v["resource"]
    client = TestClient(_load_app())
    assert client.delete(f"/{resource}/999999").status_code == 404
