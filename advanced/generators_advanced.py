"""Продвинутые генераторы и контекстные менеджеры.

send(), yield from, конвейеры обработки данных, ExitStack, асинхронные
контекстные менеджеры.

Запуск: python -m advanced.generators_advanced
"""

from __future__ import annotations

import asyncio
import re
from collections.abc import AsyncIterator, Generator, Iterable, Iterator
from contextlib import ExitStack, asynccontextmanager, contextmanager, suppress
from pathlib import Path


# --- 1. Генератор-корутина: send() --------------------------------------------
def running_average() -> Generator[float, float, None]:
    """Принимает числа через send() и отдаёт текущее среднее."""
    total = 0.0
    count = 0
    average = 0.0
    while True:
        value = yield average
        total += value
        count += 1
        average = total / count


# --- 2. yield from: делегирование и возврат значения -------------------------
def flatten(tree: Iterable) -> Iterator:
    for node in tree:
        if isinstance(node, Iterable) and not isinstance(node, (str, bytes)):
            yield from flatten(node)
        else:
            yield node


def count_and_yield(items: Iterable[str]) -> Generator[str, None, int]:
    n = 0
    for item in items:
        yield item.upper()
        n += 1
    return n  # значение попадает в StopIteration.value


def delegator(items: Iterable[str]) -> Generator[str, None, str]:
    n = yield from count_and_yield(items)  # yield from возвращает return-значение
    return f"обработано {n}"


# --- 3. Конвейер обработки логов из генераторов ------------------------------
LOG_RE = re.compile(r"(?P<level>INFO|WARNING|ERROR) (?P<service>\w+): (?P<msg>.*)")


def parse(lines: Iterable[str]) -> Iterator[dict[str, str]]:
    for line in lines:
        if m := LOG_RE.search(line):
            yield m.groupdict()


def only(level: str, records: Iterable[dict[str, str]]) -> Iterator[dict[str, str]]:
    return (r for r in records if r["level"] == level)


def count_by(key: str, records: Iterable[dict[str, str]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for r in records:
        out[r[key]] = out.get(r[key], 0) + 1
    return out


def errors_per_service(lines: Iterable[str]) -> dict[str, int]:
    # данные текут по одной строке — работает и на логах в десятки ГБ
    return count_by("service", only("ERROR", parse(lines)))


# --- 4. ExitStack: динамическое число контекстных менеджеров -----------------
def merge_files(paths: list[Path], out: Path) -> int:
    with ExitStack() as stack:
        files = [stack.enter_context(p.open(encoding="utf-8")) for p in paths]
        dst = stack.enter_context(out.open("w", encoding="utf-8"))
        lines = 0
        for f in files:
            for line in f:
                dst.write(line)
                lines += 1
        return lines  # все файлы закроются, даже при исключении


@contextmanager
def transaction(log: list[str]) -> Iterator[None]:
    log.append("BEGIN")
    try:
        yield
    except Exception:
        log.append("ROLLBACK")
        raise
    else:
        log.append("COMMIT")


# --- 5. Асинхронный контекстный менеджер -------------------------------------
class FakePool:
    def __init__(self) -> None:
        self.open = False

    async def connect(self) -> None:
        await asyncio.sleep(0)
        self.open = True

    async def close(self) -> None:
        await asyncio.sleep(0)
        self.open = False


@asynccontextmanager
async def db_pool() -> AsyncIterator[FakePool]:
    pool = FakePool()
    await pool.connect()
    try:
        yield pool
    finally:
        await pool.close()


def main() -> None:
    avg = running_average()
    next(avg)  # «прогреть» генератор до первого yield
    print([round(avg.send(x), 2) for x in (10, 20, 60)])

    print(list(flatten([1, [2, [3, (4, 5)], "abc"]])))

    gen = delegator(["a", "b"])
    print(list(gen))
    with suppress(StopIteration):
        next(gen)

    logs = [
        "2026-01-01 ERROR auth: bad token",
        "2026-01-01 INFO api: ok",
        "2026-01-01 ERROR api: timeout",
        "2026-01-01 ERROR auth: expired",
    ]
    print(errors_per_service(logs))

    log: list[str] = []
    with suppress(ValueError), transaction(log):
        raise ValueError
    print(log)

    async def use_pool() -> bool:
        async with db_pool() as pool:
            return pool.open

    print("pool открыт внутри:", asyncio.run(use_pool()))


if __name__ == "__main__":
    main()
