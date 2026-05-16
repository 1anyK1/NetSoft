"""Второй сервис за неделю 03: только маршрут /other для шлюза /api/v1/other."""

from fastapi import FastAPI

app = FastAPI(title="other-mock")


@app.get("/other")
async def read_other():
    return {"route": "/other", "role": "mock-secondary-service"}
