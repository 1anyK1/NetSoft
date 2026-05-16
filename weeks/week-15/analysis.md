# Анализ производительности (events-s01)

## Latency

Использовались синтетические прогоны `weeks/week-15/load_test.py` против REST-списка `events`.

| concurrency | наблюдаемые эффекты |
|--------------|---------------------|
| 1 | базовый round-trip без конкуренции |
| 10 | средняя **latency** растёт умеренно |
| 100 | упор в CPU/async loop; **latency** p95 может «уйти» если нет масштабирования |

Подробнее цифры зависят от железа; сохраните `last_load_summary.txt` после прогона.

## Throughput (throughput vs RPS)

С ростом одновременных клиентов RPS доходит до **точки насыщения**: дальнейшее увеличение concurrency добавляет только очередь, а коды успеха могут упираться в таймауты.

### Как воспроизвести быстрое сравнение

```bash
export LOAD_URL=http://127.0.0.1:8217/events
for c in 1 10 100; do
  echo "conc=$c"
  CONCURRENCY=$c REQUESTS=300 LOAD_URL=$LOAD_URL python weeks/week-15/load_test.py
done
```

## Вывод

Для варианта **events-s01** рост concurrency нагружает in-memory-сервис: полезно кешировать популярные `GET`, масштабировать реплики за балансировщиком и измерять gRPC там, где критичен overhead JSON.
