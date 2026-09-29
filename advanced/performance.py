"""Производительность и память: измеряйте, а не угадывайте.

__slots__, cached_property, lru_cache, weakref, tracemalloc, cProfile, timeit.

Запуск: python -m advanced.performance
"""

from __future__ import annotations

import cProfile
import io
import pstats
import sys
import timeit
import tracemalloc
import weakref
from dataclasses import dataclass
from functools import cached_property, lru_cache


# --- 1. __slots__: меньше памяти и быстрее доступ к атрибутам ----------------
class PointDict:
    def __init__(self, x: float, y: float) -> None:
        self.x, self.y = x, y


class PointSlots:
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x, self.y = x, y


@dataclass(slots=True, frozen=True)  # то же самое в dataclass
class PointDC:
    x: float
    y: float


def instance_size(obj: object) -> int:
    size = sys.getsizeof(obj)
    if hasattr(obj, "__dict__"):
        size += sys.getsizeof(obj.__dict__)
    return size


def measure_allocations(factory, n: int = 100_000) -> int:
    """Сколько байт памяти занимают n объектов (через tracemalloc)."""
    tracemalloc.start()
    snapshot_before = tracemalloc.take_snapshot()
    objs = [factory(i, i) for i in range(n)]
    snapshot_after = tracemalloc.take_snapshot()
    tracemalloc.stop()
    stats = snapshot_after.compare_to(snapshot_before, "filename")
    del objs
    return sum(s.size_diff for s in stats)


# --- 2. cached_property и lru_cache ------------------------------------------
class Dataset:
    def __init__(self, values: list[float]) -> None:
        self.values = values

    @cached_property
    def stats(self) -> dict[str, float]:
        n = len(self.values)
        mean = sum(self.values) / n
        var = sum((v - mean) ** 2 for v in self.values) / n
        return {"mean": mean, "std": var**0.5}


@lru_cache(maxsize=1024)
def edit_distance(a: str, b: str) -> int:
    """Расстояние Левенштейна — классика динамического программирования."""
    if not a:
        return len(b)
    if not b:
        return len(a)
    if a[0] == b[0]:
        return edit_distance(a[1:], b[1:])
    return 1 + min(
        edit_distance(a[1:], b),  # удаление
        edit_distance(a, b[1:]),  # вставка
        edit_distance(a[1:], b[1:]),  # замена
    )


# --- 3. weakref: кэш, не мешающий сборщику мусора ----------------------------
class Image:
    def __init__(self, name: str) -> None:
        self.name = name


class ImageCache:
    def __init__(self) -> None:
        self._cache: weakref.WeakValueDictionary[str, Image] = weakref.WeakValueDictionary()
        self.loads = 0

    def get(self, name: str) -> Image:
        img = self._cache.get(name)
        if img is None:
            self.loads += 1
            img = Image(name)
            self._cache[name] = img
        return img

    def __len__(self) -> int:
        return len(self._cache)


# --- 4. Профилирование ---------------------------------------------------------
def profile(func, *args, top: int = 5) -> str:
    pr = cProfile.Profile()
    pr.enable()
    func(*args)
    pr.disable()
    buf = io.StringIO()
    pstats.Stats(pr, stream=buf).sort_stats("cumulative").print_stats(top)
    return buf.getvalue()


def slow_concat(n: int) -> str:
    s = ""
    for i in range(n):
        s += str(i)
    return s


def fast_join(n: int) -> str:
    return "".join(map(str, range(n)))


def main() -> None:
    print("Размер экземпляра:", instance_size(PointDict(1, 2)), "vs", instance_size(PointSlots(1, 2)))
    print("100k объектов, байт:", measure_allocations(PointDict), "vs", measure_allocations(PointSlots))

    d = Dataset([1, 2, 3, 4, 5])
    print(d.stats, d.stats is d.stats)
    print("Левенштейн:", edit_distance("котёнок", "кашалот"), edit_distance.cache_info())

    cache = ImageCache()
    a = cache.get("logo.png")
    cache.get("logo.png")
    print("Загрузок:", cache.loads, "в кэше:", len(cache))
    del a
    print("После del в кэше:", len(cache))  # 0 — объект собран

    for fn in (slow_concat, fast_join):
        t = timeit.timeit(lambda: fn(10_000), number=50)
        print(f"{fn.__name__}: {t:.3f} с")

    print(profile(edit_distance.__wrapped__, "профилирование", "оптимизация"))


if __name__ == "__main__":
    main()
