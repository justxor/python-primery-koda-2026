"""contextvars: «глобальные» переменные, безопасные для asyncio и потоков.

Типичный случай — request_id / user_id, который нужно видеть в логах
глубоко в коде, не передавая его через все функции.

Запуск: python -m advanced.contextvars_demo
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar

request_id: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIdFilter(logging.Filter):
    """Добавляет request_id в каждую запись лога."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id.get()
        return True


def setup_logging() -> logging.Logger:
    logger = logging.getLogger("app")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.addFilter(RequestIdFilter())
        handler.setFormatter(logging.Formatter("%(request_id)s | %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


@contextmanager
def bind_request_id(value: str | None = None) -> Iterator[str]:
    token = request_id.set(value or uuid.uuid4().hex[:8])
    try:
        yield request_id.get()
    finally:
        request_id.reset(token)  # всегда восстанавливаем прежнее значение


async def repository_call() -> str:
    await asyncio.sleep(0.01)
    # функция ничего не знает о запросе, но видит его id
    return request_id.get()


async def handle_request(rid: str, log: logging.Logger) -> str:
    with bind_request_id(rid):
        log.info("начало обработки")
        seen = await repository_call()
        log.info("конец обработки")
        return seen


async def main() -> None:
    log = setup_logging()
    # каждая задача получает КОПИЮ контекста — значения не смешиваются
    results = await asyncio.gather(*(handle_request(f"req-{i}", log) for i in range(3)))
    print(results, "| снаружи:", request_id.get())


if __name__ == "__main__":
    asyncio.run(main())
