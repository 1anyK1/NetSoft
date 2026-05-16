"""
Минимальный signaling-сервер для WebRTC (README недели 09).
Клиенты на одном WebSocket-эндпоинте рассылают сырой текст друг другу — достаточно для обмена SDP / ICE.


    uvicorn signaling_server:app --app-dir weeks/week-09 --host 0.0.0.0 --port 8765
"""

from __future__ import annotations

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI(title="webrtc-signaling")
_CONNECTIONS: set[WebSocket] = set()


@app.websocket("/ws")
async def relay(websocket: WebSocket) -> None:
    await websocket.accept()
    _CONNECTIONS.add(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            for peer in list(_CONNECTIONS):
                if peer is not websocket:
                    await peer.send_text(message)
    except WebSocketDisconnect:
        pass
    finally:
        _CONNECTIONS.discard(websocket)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "connections": str(len(_CONNECTIONS))}
