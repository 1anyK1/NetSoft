import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Response
from pydantic import create_model

ROOT = Path(__file__).resolve().parents[3]


def _load_variant(week: str) -> dict:
    group = os.getenv("GROUP", "332")
    student_id = os.getenv("STUDENT_ID", "s01")
    path = ROOT / "variants" / group / student_id / f"week-{week}.json"
    return json.loads(path.read_text())


_v = _load_variant("02")
RESOURCE = _v["resource"]
_extra = _v["extra_field"]
_EXTRA_NAME = _extra["name"]
_TYPE_MAP = {"str": str, "int": int, "float": float, "bool": bool}
_ExtraT = _TYPE_MAP[_extra["type"]]

_CreateModel = create_model(
    "CreateItem",
    name=(str, ...),
    **{_EXTRA_NAME: (_ExtraT, ...)},
)

_UpdateModel = create_model(
    "UpdateItem",
    name=(str, ...),
    **{_EXTRA_NAME: (_ExtraT, ...)},
)

app = FastAPI()
_store: dict[int, dict] = {}
_next_id = 1


@app.get(f"/{RESOURCE}")
def list_items():
    return list(_store.values())


@app.post(f"/{RESOURCE}", status_code=201)
def create_item(body: _CreateModel):
    global _next_id
    rid = _next_id
    _next_id += 1
    data = {"id": rid, "name": body.name, _EXTRA_NAME: getattr(body, _EXTRA_NAME)}
    _store[rid] = data
    return data


@app.get(f"/{RESOURCE}/{{item_id}}")
def get_item(item_id: int):
    if item_id not in _store:
        raise HTTPException(status_code=404, detail="Not found")
    return _store[item_id]


@app.put(f"/{RESOURCE}/{{item_id}}")
def update_item(item_id: int, body: _UpdateModel):
    if item_id not in _store:
        raise HTTPException(status_code=404, detail="Not found")
    _store[item_id] = {
        "id": item_id,
        "name": body.name,
        _EXTRA_NAME: getattr(body, _EXTRA_NAME),
    }
    return _store[item_id]


@app.delete(f"/{RESOURCE}/{{item_id}}")
def delete_item(item_id: int):
    if item_id not in _store:
        raise HTTPException(status_code=404, detail="Not found")
    del _store[item_id]
    return Response(status_code=204)
