"""Тесты для задач 8–13. Запуск: pytest -q"""

from __future__ import annotations

import asyncio
import itertools

import pytest

from advanced import tasks_senior as ts


def test_ttl_cache_expires_and_evicts() -> None:
    now = [0.0]
    calls: list[int] = []

    @ts.ttl_cache(ttl=10, maxsize=2, clock=lambda: now[0])
    def f(x: int) -> int:
        calls.append(x)
        return x * 2

    assert f(1) == f(1) == 2
    assert calls == [1]
    now[0] = 11  # запись протухла
    f(1)
    assert calls == [1, 1]
    f(2)
    f(3)  # вытесняет 1 (maxsize=2)
    f(1)
    assert calls == [1, 1, 2, 3, 1]


def test_batcher_groups_and_dedupes() -> None:
    async def fetch(ids: list[int]) -> dict[int, str]:
        await asyncio.sleep(0)
        return {i: f"u{i}" for i in ids if i != 404}

    async def scenario() -> tuple[list[str], list[list[int]], bool]:
        loader = ts.Batcher(fetch, max_batch=3)
        res = await asyncio.gather(*(loader.load(i) for i in [1, 2, 1, 3, 4]))
        try:
            await loader.load(404)
            missing = False
        except KeyError:
            missing = True
        return list(res), loader.batches, missing

    res, batches, missing = asyncio.run(scenario())
    assert res == ["u1", "u2", "u1", "u3", "u4"]
    assert batches[:2] == [[1, 2, 3], [4]]  # дубликат 1 не попал в батч
    assert missing


def test_install_order() -> None:
    deps = {"app": ["web", "db"], "web": ["http"], "db": ["driver"], "http": []}
    order = ts.install_order(deps)
    for node, reqs in deps.items():
        for r in reqs:
            assert order.index(r) < order.index(node)
    with pytest.raises(ts.CycleError):
        ts.install_order({"a": ["b"], "b": ["c"], "c": ["a"]})


def test_trie_suggest() -> None:
    t = ts.Trie()
    for w, n in {"python": 10, "pytest": 7, "pydantic": 7, "pandas": 8, "py": 1}.items():
        t.add(w, n)
    assert t.suggest("py", 3) == ["python", "pydantic", "pytest"]
    assert t.suggest("pa") == ["pandas"]
    assert t.suggest("java") == []


def test_hash_ring_moves_few_keys() -> None:
    ring = ts.HashRing(["a", "b", "c"])
    keys = [f"k{i}" for i in range(2000)]
    before = {k: ring.get(k) for k in keys}
    ring.add("d")
    moved = sum(before[k] != ring.get(k) for k in keys)
    assert 0.1 < moved / len(keys) < 0.4  # в идеале ~25%
    assert all(ring.get(k) == "d" for k in keys if before[k] != ring.get(k))
    ring.remove("d")
    assert {k: ring.get(k) for k in keys} == before
    with pytest.raises(LookupError):
        ts.HashRing().get("x")


def test_merge_sorted() -> None:
    assert list(ts.merge_sorted([1, 4, 9], [], [2, 3, 10], [5])) == [1, 2, 3, 4, 5, 9, 10]
    words = ts.merge_sorted(["bb", "dddd"], ["a", "ccc"], key=len)
    assert list(words) == ["a", "bb", "ccc", "dddd"]
    evens = itertools.count(0, 2)  # бесконечные потоки
    odds = itertools.count(1, 2)
    assert list(itertools.islice(ts.merge_sorted(evens, odds), 6)) == [0, 1, 2, 3, 4, 5]
