import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Response
from pydantic import create_model

REPO_ROOT = Path(__file__).resolve().parents[3]


def _load_variant_week(week: str) -> dict:
    group = os.getenv("GROUP", "332")
    student_id = os.getenv("STUDENT_ID", "s01")
    path = REPO_ROOT / "variants" / group / student_id / f"week-{week}.json"
    return json.loads(path.read_text())


_v = _load_variant_week("11")
RESOURCE = _v["resource"]
_extra = _v["extra_field"]
_EXTRA_NAME = _extra["name"]
_TYPE_MAP = {"str": str, "int": int, "float": float, "bool": bool}
_ExtraT = _TYPE_MAP[_extra["type"]]

_CreateModel = create_model(
    "CreateDoc",
    name=(str, ...),
    **{_EXTRA_NAME: (_ExtraT, ...)},
)

_UpdateModel = create_model(
    "UpdateDoc",
    name=(str, ...),
    **{_EXTRA_NAME: (_ExtraT, ...)},
)

app = FastAPI(title=_v["project_code"])
_store: dict[int, dict] = {}
_next_id = 1

API_PREFIX = f"/api/{RESOURCE}"


@app.get("/health")
def health():
    return {"status": "ok", "service": _v["service"]["name"]}


@app.get(API_PREFIX)
def list_logs():
    return list(_store.values())


@app.post(API_PREFIX, status_code=201)
def create_doc(body: _CreateModel):
    global _next_id
    rid = _next_id
    _next_id += 1
    rec = {"id": rid, "name": body.name, _EXTRA_NAME: getattr(body, _EXTRA_NAME)}
    _store[rid] = rec
    return rec


@app.get(f"{API_PREFIX}/{{rid}}")
def get_doc(rid: int):
    if rid not in _store:
        raise HTTPException(404, "Not found")
    return _store[rid]


@app.put(f"{API_PREFIX}/{{rid}}")
def put_doc(rid: int, body: _UpdateModel):
    if rid not in _store:
        raise HTTPException(404, "Not found")
    _store[rid] = {"id": rid, "name": body.name, _EXTRA_NAME: getattr(body, _EXTRA_NAME)}
    return _store[rid]


@app.delete(f"{API_PREFIX}/{{rid}}")
def del_doc(rid: int):
    if rid not in _store:
        raise HTTPException(404, "Not found")
    del _store[rid]
    return Response(status_code=204)


@app.get("/")
def root():
    return {"week": "11", "project": _v["project_code"]}
