"""Решения задач уровня middle+ / senior из README (задачи 8–13).

Запуск: python -m advanced.tasks_senior
"""

from __future__ import annotations

import asyncio
import bisect
import functools
import hashlib
import heapq
import time
from collections import OrderedDict, defaultdict, deque
from collections.abc import Awaitable, Callable, Hashable, Iterable, Iterator
from typing import Any


# --- Задача 8. TTL-кэш с ограничением размера --------------------------------
def ttl_cache(
    ttl: float, maxsize: int = 128, clock: Callable[[], float] = time.monotonic
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        data: OrderedDict[Hashable, tuple[float, Any]] = OrderedDict()

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, tuple(sorted(kwargs.items())))
            now = clock()
            if key in data:
                expires, value = data[key]
                if expires > now:
                    data.move_to_end(key)
                    return value
                del data[key]  # запись протухла
            value = func(*args, **kwargs)
            data[key] = (now + ttl, value)
            if len(data) > maxsize:
                data.popitem(last=False)  # вытесняем самую старую
            return value

        wrapper.cache_clear = data.clear  # type: ignore[attr-defined]
        return wrapper

    return decorator


# --- Задача 9. Асинхронный батчер (DataLoader) -------------------------------
class Batcher[K, V]:
    """Собирает одиночные запросы load(key), пришедшие почти одновременно,
    в один вызов batch_fn(keys) — решение проблемы N+1 запросов."""

    def __init__(
        self,
        batch_fn: Callable[[list[K]], Awaitable[dict[K, V]]],
        max_batch: int = 100,
        delay: float = 0.005,
    ) -> None:
        self.batch_fn = batch_fn
        self.max_batch = max_batch
        self.delay = delay
        self._pending: dict[K, asyncio.Future[V]] = {}
        self._timer: asyncio.TimerHandle | None = None
        self.batches: list[list[K]] = []

    def load(self, key: K) -> asyncio.Future[V]:
        if key in self._pending:  # дедупликация одинаковых ключей
            return self._pending[key]
        loop = asyncio.get_running_loop()
        fut: asyncio.Future[V] = loop.create_future()
        self._pending[key] = fut
        if len(self._pending) >= self.max_batch:
            self._flush()
        elif self._timer is None:
            self._timer = loop.call_later(self.delay, self._flush)
        return fut

    def _flush(self) -> None:
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None
        pending, self._pending = self._pending, {}
        if pending:
            asyncio.get_running_loop().create_task(self._dispatch(pending))

    async def _dispatch(self, pending: dict[K, asyncio.Future[V]]) -> None:
        keys = list(pending)
        self.batches.append(keys)
        try:
            result = await self.batch_fn(keys)
        except Exception as exc:
            for fut in pending.values():
                fut.set_exception(exc)
            return
        for key, fut in pending.items():
            if key in result:
                fut.set_result(result[key])
            else:
                fut.set_exception(KeyError(key))


# --- Задача 10. Порядок установки зависимостей (топологическая сортировка) ---
class CycleError(ValueError):
    pass


def install_order(deps: dict[str, Iterable[str]]) -> list[str]:
    """Алгоритм Кана: O(V + E). deps[x] — от чего зависит x."""
    graph: defaultdict[str, list[str]] = defaultdict(list)
    indegree: dict[str, int] = {}
    for node, requires in deps.items():
        indegree.setdefault(node, 0)
        for req in requires:
            indegree.setdefault(req, 0)
            graph[req].append(node)
            indegree[node] += 1

    queue = deque(sorted(n for n, d in indegree.items() if d == 0))
    order: list[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in sorted(graph[node]):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    if len(order) != len(indegree):
        cyclic = sorted(n for n, d in indegree.items() if d > 0)
        raise CycleError(f"Циклическая зависимость: {cyclic}")
    return order


# --- Задача 11. Автодополнение на префиксном дереве (Trie) -------------------
class Trie:
    __slots__ = ("children", "count")

    def __init__(self) -> None:
        self.children: dict[str, Trie] = {}
        self.count = 0  # сколько раз слово встретилось (0 — не конец слова)

    def add(self, word: str, times: int = 1) -> None:
        node = self
        for ch in word:
            node = node.children.setdefault(ch, Trie())
        node.count += times

    def suggest(self, prefix: str, limit: int = 5) -> list[str]:
        node = self
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]

        found: list[tuple[int, str]] = []
        stack = [(node, prefix)]
        while stack:
            cur, word = stack.pop()
            if cur.count:
                found.append((-cur.count, word))
            stack.extend((child, word + ch) for ch, child in cur.children.items())
        # самые частые, при равенстве — по алфавиту
        return [w for _, w in heapq.nsmallest(limit, found)]


# --- Задача 12. Консистентное хеширование -------------------------------------
class HashRing:
    """При добавлении/удалении сервера переезжает лишь ~1/N ключей,
    а не почти все, как при hash(key) % N."""

    def __init__(self, nodes: Iterable[str] = (), replicas: int = 100) -> None:
        self.replicas = replicas
        self._ring: list[tuple[int, str]] = []
        for node in nodes:
            self.add(node)

    @staticmethod
    def _hash(value: str) -> int:
        return int.from_bytes(hashlib.blake2b(value.encode(), digest_size=8).digest())

    def add(self, node: str) -> None:
        for i in range(self.replicas):  # виртуальные узлы сглаживают нагрузку
            bisect.insort(self._ring, (self._hash(f"{node}#{i}"), node))

    def remove(self, node: str) -> None:
        self._ring = [item for item in self._ring if item[1] != node]

    def get(self, key: str) -> str:
        if not self._ring:
            raise LookupError("Кольцо пустое")
        idx = bisect.bisect(self._ring, (self._hash(key), ""))
        return self._ring[idx % len(self._ring)][1]


# --- Задача 13. Слияние K отсортированных потоков -----------------------------
def merge_sorted[T](*streams: Iterable[T], key: Callable[[T], Any] | None = None) -> Iterator[T]:
    """Ленивое слияние: O(N log K) по времени и O(K) по памяти.
    Потоки могут быть бесконечными генераторами или огромными файлами."""
    keyf = key or (lambda x: x)
    heap: list[tuple[Any, int, T, Iterator[T]]] = []
    for idx, stream in enumerate(streams):
        it = iter(stream)
        for first in it:
            heap.append((keyf(first), idx, first, it))
            break
    heapq.heapify(heap)
    while heap:
        _, idx, value, it = heap[0]
        yield value
        for nxt in it:
            heapq.heapreplace(heap, (keyf(nxt), idx, nxt, it))
            break
        else:
            heapq.heappop(heap)


def main() -> None:
    @ttl_cache(ttl=60)
    def slow_square(x: int) -> int:
        time.sleep(0.1)
        return x * x

    slow_square(9)
    start = time.perf_counter()
    slow_square(9)
    print(f"TTL-кэш: повтор за {time.perf_counter() - start:.4f} с")

    async def fetch_users(ids: list[int]) -> dict[int, str]:
        await asyncio.sleep(0.01)
        return {i: f"user{i}" for i in ids}

    async def demo_batcher() -> None:
        loader = Batcher(fetch_users)
        users = await asyncio.gather(*(loader.load(i) for i in [1, 2, 3, 2, 1]))
        print("Батчер:", users, "запросов к БД:", len(loader.batches))

    asyncio.run(demo_batcher())

    print(install_order({"app": ["web", "db"], "web": ["http"], "db": ["driver"], "http": []}))

    trie = Trie()
    for word, freq in {"python": 10, "pytest": 7, "pydantic": 5, "pandas": 8}.items():
        trie.add(word, freq)
    print("Подсказки для 'py':", trie.suggest("py", 2))

    ring = HashRing(["cache-1", "cache-2", "cache-3"])
    keys = [f"user:{i}" for i in range(1000)]
    before = {k: ring.get(k) for k in keys}
    ring.add("cache-4")
    moved = sum(before[k] != ring.get(k) for k in keys)
    print(f"Консистентное хеширование: переехало {moved / 10:.1f}% ключей")

    print(list(merge_sorted([1, 4, 9], [2, 3, 10], [5])))


if __name__ == "__main__":
    main()
