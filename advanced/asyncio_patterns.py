"""Продвинутый asyncio: ограничение параллелизма, таймауты, очереди,
отмена, асинхронные генераторы и повтор с экспоненциальной задержкой.

Запуск: python -m advanced.asyncio_patterns
"""

from __future__ import annotations

import asyncio
import random
from collections.abc import AsyncIterator, Awaitable, Callable, Iterable


# --- 1. Ограничение числа одновременных задач (Semaphore + TaskGroup) --------
async def gather_limited[T](
    coros: Iterable[Awaitable[T]], limit: int
) -> list[T]:
    """Как asyncio.gather, но не более `limit` задач одновременно.
    Порядок результатов совпадает с порядком входных корутин."""
    sem = asyncio.Semaphore(limit)

    async def run(coro: Awaitable[T]) -> T:
        async with sem:
            return await coro

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(run(c)) for c in coros]
    return [t.result() for t in tasks]


# --- 2. Повтор с экспоненциальной задержкой и джиттером ----------------------
async def retry_async[T](
    func: Callable[[], Awaitable[T]],
    *,
    attempts: int = 5,
    base_delay: float = 0.1,
    max_delay: float = 5.0,
    retry_on: tuple[type[BaseException], ...] = (ConnectionError, TimeoutError),
) -> T:
    for attempt in range(attempts):
        try:
            return await func()
        except retry_on:
            if attempt == attempts - 1:
                raise
            delay = min(max_delay, base_delay * 2**attempt)
            await asyncio.sleep(random.uniform(0, delay))  # full jitter
    raise AssertionError("unreachable")


# --- 3. Producer / consumer через asyncio.Queue ------------------------------
async def process_queue[T, R](
    items: Iterable[T],
    handler: Callable[[T], Awaitable[R]],
    workers: int = 3,
) -> list[R]:
    queue: asyncio.Queue[T] = asyncio.Queue(maxsize=workers * 2)  # backpressure
    results: list[R] = []

    async def worker() -> None:
        while True:
            item = await queue.get()
            try:
                results.append(await handler(item))
            finally:
                queue.task_done()

    async with asyncio.TaskGroup() as tg:
        worker_tasks = [tg.create_task(worker()) for _ in range(workers)]
        for item in items:
            await queue.put(item)
        await queue.join()  # ждём, пока все элементы обработаны
        for t in worker_tasks:
            t.cancel()  # воркеры бесконечны — останавливаем явно
    return results


# --- 4. Таймауты: asyncio.timeout (3.11+) ------------------------------------
async def fetch_with_deadline(delay: float, deadline: float) -> str | None:
    try:
        async with asyncio.timeout(deadline):
            await asyncio.sleep(delay)
            return "готово"
    except TimeoutError:
        return None


# --- 5. Асинхронный генератор + корректное освобождение ресурсов ------------
async def ticker(interval: float, limit: int) -> AsyncIterator[int]:
    try:
        for i in range(limit):
            yield i
            await asyncio.sleep(interval)
    finally:
        # сработает и при break в async for (через aclose)
        print("ticker: закрыт")


# --- 6. Отмена, которую нельзя прервать: shield ------------------------------
async def save_to_db(log: list[str]) -> None:
    await asyncio.sleep(0.05)
    log.append("сохранено")


async def handler_with_shield(log: list[str]) -> None:
    # даже если внешнюю задачу отменят, запись в БД завершится
    await asyncio.shield(save_to_db(log))


# --- 7. Запуск блокирующего кода без блокировки event loop -------------------
def blocking_io(n: int) -> int:
    import time

    time.sleep(0.05)
    return n * 2


async def run_blocking() -> list[int]:
    return list(await asyncio.gather(*(asyncio.to_thread(blocking_io, i) for i in range(5))))


async def main() -> None:
    async def job(i: int) -> int:
        await asyncio.sleep(random.random() / 20)
        return i * i

    print(await gather_limited((job(i) for i in range(10)), limit=3))
    print(sorted(await process_queue(range(8), job, workers=2)))
    print(await fetch_with_deadline(0.01, 1), await fetch_with_deadline(1, 0.01))

    async for tick in ticker(0.01, 100):
        if tick == 2:
            break

    print(await run_blocking())


if __name__ == "__main__":
    asyncio.run(main())
