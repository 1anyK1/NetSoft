"""
gRPC-сервер по условию README неделей 07–08: Unary Ping + серверный стрим Subscribe.
Запуск: из каталога week-07: python grpc_server.py
Порт по умолчанию: 50051
"""

from __future__ import annotations

import concurrent.futures
import sys
from pathlib import Path

GEN = Path(__file__).resolve().parent / "gen"
sys.path.insert(0, str(GEN))

import grpc  # noqa: E402
import service_pb2  # noqa: E402
import service_pb2_grpc  # noqa: E402


class NotificationsServicer(service_pb2_grpc.NotificationsServiceServicer):
    def Ping(self, request, context):  # noqa: N802 (имя из .proto/grpc)
        return service_pb2.PingResponse(message=f"pong-{request.client_id}")

    def Subscribe(self, request, context):  # noqa: N802
        chan = request.channel or "default"
        for seq in range(5):
            yield service_pb2.NotificationEvent(text=f"{chan}-{seq}", seq=seq)


def serve(port: int = 50051) -> None:
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=8))
    service_pb2_grpc.add_NotificationsServiceServicer_to_server(NotificationsServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"gRPC NotificationsService listens on :{port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
