"""Параллелизм: потоки, процессы, free-threaded Python и субинтерпретаторы.

Шпаргалка:
* I/O-bound (сеть, диск)      → asyncio или ThreadPoolExecutor
* CPU-bound (вычисления)      → ProcessPoolExecutor,
                                 free-threaded сборка 3.13t/3.14t + потоки,
                                 или InterpreterPoolExecutor (3.14+)

Запуск: python -m advanced.concurrency
"""

from __future__ import annotations

import concurrent.futures as cf
import sys
import sysconfig
import threading
import time
from collections.abc import Callable, Iterable


def gil_status() -> str:
    """Проверить, собран ли интерпретатор без GIL и включён ли GIL сейчас."""
    free_threaded_build = bool(sysconfig.get_config_var("Py_GIL_DISABLED"))
    gil_enabled = getattr(sys, "_is_gil_enabled", lambda: True)()
    return f"free-threaded сборка: {free_threaded_build}, GIL включён: {gil_enabled}"


def cpu_task(n: int) -> int:
    """Намеренно «тяжёлая» функция для демонстрации."""
    total = 0
    for i in range(n):
        total += i * i % 7
    return total


def run_pool[T, R](
    executor_cls: type[cf.Executor], func: Callable[[T], R], items: Iterable[T], workers: int = 4
) -> tuple[list[R], float]:
    start = time.perf_counter()
    with executor_cls(max_workers=workers) as ex:
        results = list(ex.map(func, items))
    return results, time.perf_counter() - start


def best_executor() -> type[cf.Executor]:
    """Лучший пул для CPU-задач в текущем интерпретаторе."""
    if not getattr(sys, "_is_gil_enabled", lambda: True)():
        return cf.ThreadPoolExecutor  # GIL выключен → потоки параллельны
    if hasattr(cf, "InterpreterPoolExecutor"):  # Python 3.14+
        return cf.InterpreterPoolExecutor
    return cf.ProcessPoolExecutor


# --- Потокобезопасный счётчик -------------------------------------------------
class Counter:
    """`self.value += 1` — не атомарная операция. Без Lock, особенно
    в free-threaded Python, счётчик потеряет инкременты."""

    def __init__(self) -> None:
        self.value = 0
        self._lock = threading.Lock()

    def increment(self) -> None:
        with self._lock:
            self.value += 1


def hammer(counter: Counter, threads: int = 8, per_thread: int = 10_000) -> int:
    def work() -> None:
        for _ in range(per_thread):
            counter.increment()

    ts = [threading.Thread(target=work) for _ in range(threads)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return counter.value


# --- as_completed: обрабатываем результаты по мере готовности ----------------
def first_n_completed(func: Callable[[int], int], items: list[int], n: int) -> list[int]:
    out: list[int] = []
    with cf.ThreadPoolExecutor() as ex:
        futures = [ex.submit(func, i) for i in items]
        for fut in cf.as_completed(futures):
            out.append(fut.result())
            if len(out) == n:
                for f in futures:
                    f.cancel()  # отменит ещё не начатые
                break
    return out


def main() -> None:
    print(gil_status())
    items = [2_000_000] * 4
    for cls in (cf.ThreadPoolExecutor, cf.ProcessPoolExecutor, best_executor()):
        _, elapsed = run_pool(cls, cpu_task, items)
        print(f"{cls.__name__:<26} {elapsed:.2f} с")
    print("Счётчик:", hammer(Counter()))


if __name__ == "__main__":
    main()
