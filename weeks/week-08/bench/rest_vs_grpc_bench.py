#!/usr/bin/env python3
"""
Бенчмарк по README недели 08: серия Unary-вызовов REST против gRPC.

Перед запуском должен быть доступен gRPC-сервер недели 07 (`grpc_server.py`).
REST — любой быстрый GET из недель 01–02 на вашей машине.

Пример:

    export GRPC_TARGET=127.0.0.1:50051
    export REST_URL=http://127.0.0.1:9275/photos
    python weeks/week-08/bench/rest_vs_grpc_bench.py
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import requests

WK7_GEN = Path(__file__).resolve().parents[2] / "week-07" / "gen"
sys.path.insert(0, str(WK7_GEN))

REST_URL = os.environ.get("REST_URL")
GRPC_TARGET = os.environ.get("GRPC_TARGET", "127.0.0.1:50051")

N = int(os.environ.get("BENCH_ITERATIONS", "1000"))


def bench_rest(url: str) -> float | None:
    try:
        t0 = time.perf_counter()
        for _ in range(N):
            r = requests.get(url, timeout=5)
            r.raise_for_status()
        return time.perf_counter() - t0
    except Exception as exc:  # noqa: BLE001
        print("REST недоступен:", exc)
        return None


def bench_grpc_ping() -> float | None:
    try:
        import grpc  # noqa: WPS433
        import service_pb2  # type: ignore
        import service_pb2_grpc  # type: ignore
    except Exception as exc:  # noqa: BLE001
        print("Не удалось импортировать gRPC-артефакты:", exc)
        return None

    try:
        t0 = time.perf_counter()
        with grpc.insecure_channel(GRPC_TARGET) as ch:
            stub = service_pb2_grpc.NotificationsServiceStub(ch)
            for _ in range(N):
                stub.Ping(service_pb2.PingRequest(client_id="bench"))
        return time.perf_counter() - t0
    except Exception as exc:  # noqa: BLE001
        print("gRPC недоступен:", exc)
        return None


def main() -> None:
    rt = bench_rest(REST_URL) if REST_URL else None
    gt = bench_grpc_ping()

    lines: list[str] = []
    if rt is not None:
        lines.append(f"REST {N} GET: {rt:.4f}s (url={REST_URL})")
    if gt is not None:
        lines.append(f"gRPC {N} Unary Ping: {gt:.4f}s (target={GRPC_TARGET})")
    if rt and gt:
        lines.append(f"REST/gRPC time ratio ~ {(rt / gt):.2f}x")

    out = "\n".join(lines)
    if not out:
        out = (
            "Нет результатов: задайте REST_URL до вашего локального сервера "
            "(недели 01–02) и запустите weeks/week-07/grpc_server.py."
        )
    print(out)

    summary = Path(__file__).resolve().parent / "last_run_seconds.txt"
    summary.write_text(out + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
