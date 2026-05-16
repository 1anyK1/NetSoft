#!/usr/bin/env python3
"""
Нагрузочный скрипт по README недели 15 — простой синтетический профиль concurrency.

Поднимите локальный сервис (REST) и передайте URL.

    export LOAD_URL=http://127.0.0.1:8217/events
    export CONCURRENCY=50
    export REQUESTS=500
    python weeks/week-15/load_test.py

Результаты также полезно сверять с инструментами wrk/ab/ghz для отчёта.
"""

from __future__ import annotations

import asyncio
import os
import statistics
import time
from pathlib import Path

import httpx

LOAD_URL = os.environ["LOAD_URL"]  # required
TOTAL = int(os.environ.get("REQUESTS", "300"))
WORKERS = int(os.environ.get("CONCURRENCY", "10"))

latencies_ms: list[float] = []
errors = 0


async def worker(barrier: asyncio.Barrier, client: httpx.AsyncClient) -> None:
    global errors
    await barrier.wait()
    for _ in range(TOTAL // WORKERS):
        t0 = time.perf_counter()
        try:
            r = await client.get(LOAD_URL, timeout=10.0)
            r.raise_for_status()
            latencies_ms.append((time.perf_counter() - t0) * 1000)
        except Exception:  # noqa: BLE001
            errors += 1


async def main() -> None:
    barrier = asyncio.Barrier(WORKERS)
    async with httpx.AsyncClient() as client:
        start = time.perf_counter()
        await asyncio.gather(*(worker(barrier, client) for _ in range(WORKERS)))
        wall = time.perf_counter() - start

    if not latencies_ms:
        raise SystemExit("Нет успешных ответов — проверьте LOAD_URL.")

    avg = statistics.mean(latencies_ms)
    p95 = sorted(latencies_ms)[max(0, int(len(latencies_ms) * 0.95) - 1)]
    rps = len(latencies_ms) / wall
    summary = (
        f"Concurrency={WORKERS}, successful={len(latencies_ms)}, errors={errors}, wall={wall:.3f}s, "
        f"avg_latency_ms={avg:.2f}, p95_latency_ms={p95:.2f}, est_rps={rps:.1f}"
    )
    print(summary)
    Path(__file__).with_name("last_load_summary.txt").write_text(summary + "\n", encoding="utf-8")


if __name__ == "__main__":
    asyncio.run(main())
