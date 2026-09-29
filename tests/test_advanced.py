"""Тесты для продвинутых примеров. Запуск: pytest -q"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import pytest

from advanced import (
    asyncio_patterns as ap,
    concurrency,
    contextvars_demo as cv,
    descriptors,
    generators_advanced as gen,
    metaprogramming as meta,
    patterns,
    performance as perf,
    python314,
    typing_advanced as ta,
)


# --- дескрипторы -------------------------------------------------------------
def test_validated_descriptor_rejects_bad_values() -> None:
    p = descriptors.Product("Книга", 500, 3)
    assert p.total == 1500
    with pytest.raises(ValueError, match="price"):
        p.price = 0
    with pytest.raises(ValueError, match="name"):
        descriptors.Product("  ", 1, 1)


def test_lazy_computes_once() -> None:
    descriptors.Report.calls = 0
    r = descriptors.Report()
    assert r.data == r.data == [0, 1, 4, 9, 16]
    assert descriptors.Report.calls == 1


# --- метапрограммирование -----------------------------------------------------
def test_exporter_registry() -> None:
    assert {"json", "csv"} <= set(meta.Exporter.registry)
    assert meta.Exporter.for_format("csv").export({"a": 1, "b": 2}) == "a,b\n1,2"
    with pytest.raises(TypeError):

        class Duplicate(meta.Exporter, fmt="json"):
            pass

    with pytest.raises(ValueError):
        meta.Exporter.for_format("xml")


def test_singleton_and_dynamic_class() -> None:
    assert meta.Settings() is meta.Settings()
    Point = meta.make_record("Point", "x", "y")
    assert repr(Point(1, 2)) == "Point(x=1, y=2)"
    with pytest.raises(TypeError):
        Point(1)


# --- типизация -----------------------------------------------------------------
def test_typing_helpers() -> None:
    assert ta.first([], default="x") == "x"
    assert ta.clamp(-5, 0, 10) == 0
    assert list(ta.Stack[int]().push(1).push(2)) == [2, 1]
    assert ta.max_item(["b", "c", "a"]) == "c"
    assert isinstance(ta.Connection(), ta.SupportsClose)
    assert ta.parse("3.5", "float") == 3.5
    assert ta.parse("да", "bool") is True
    assert ta.voices([ta.Cat("Мурка"), ta.Dog("Шарик")]) == ["Мурка: мяу"]


def test_paramspec_decorator_keeps_metadata() -> None:
    assert ta.greet.__name__ == "greet"
    assert ta.greet("Ира") == "Привет, Ира."


# --- asyncio -------------------------------------------------------------------
def test_gather_limited_respects_limit() -> None:
    running = peak = 0

    async def job(i: int) -> int:
        nonlocal running, peak
        running += 1
        peak = max(peak, running)
        await asyncio.sleep(0.01)
        running -= 1
        return i

    result = asyncio.run(ap.gather_limited((job(i) for i in range(10)), limit=3))
    assert result == list(range(10))
    assert peak <= 3


def test_retry_async_eventually_succeeds() -> None:
    attempts = 0

    async def flaky() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ConnectionError
        return "ok"

    assert asyncio.run(ap.retry_async(flaky, base_delay=0.001)) == "ok"
    assert attempts == 3


def test_retry_async_gives_up() -> None:
    async def always_fail() -> None:
        raise TimeoutError

    with pytest.raises(TimeoutError):
        asyncio.run(ap.retry_async(always_fail, attempts=2, base_delay=0.001))


def test_process_queue_and_timeout() -> None:
    async def double(x: int) -> int:
        await asyncio.sleep(0)
        return x * 2

    assert sorted(asyncio.run(ap.process_queue(range(10), double, workers=3))) == [
        x * 2 for x in range(10)
    ]
    assert asyncio.run(ap.fetch_with_deadline(1, 0.01)) is None


def test_shield_survives_cancel() -> None:
    async def scenario() -> list[str]:
        log: list[str] = []
        task = asyncio.create_task(ap.handler_with_shield(log))
        await asyncio.sleep(0.01)
        task.cancel()
        await asyncio.sleep(0.1)
        return log

    assert asyncio.run(scenario()) == ["сохранено"]


# --- параллелизм -------------------------------------------------------------
def test_thread_safe_counter() -> None:
    assert concurrency.hammer(concurrency.Counter(), threads=4, per_thread=1000) == 4000


def test_first_n_completed() -> None:
    assert len(concurrency.first_n_completed(lambda x: x, list(range(20)), 5)) == 5


# --- contextvars ---------------------------------------------------------------
def test_request_id_isolated_between_tasks() -> None:
    log = cv.setup_logging()

    async def run() -> list[str]:
        return await asyncio.gather(*(cv.handle_request(f"r{i}", log) for i in range(5)))

    assert asyncio.run(run()) == [f"r{i}" for i in range(5)]
    assert cv.request_id.get() == "-"


# --- производительность -----------------------------------------------------
def test_slots_are_smaller() -> None:
    assert perf.instance_size(perf.PointSlots(1, 2)) < perf.instance_size(perf.PointDict(1, 2))
    assert not hasattr(perf.PointSlots(1, 2), "__dict__")


def test_edit_distance() -> None:
    assert perf.edit_distance("kitten", "sitting") == 3
    assert perf.edit_distance("", "abc") == 3


def test_weak_cache_releases_objects() -> None:
    import gc

    cache = perf.ImageCache()
    img = cache.get("a.png")
    assert cache.get("a.png") is img and cache.loads == 1
    del img
    gc.collect()
    assert len(cache) == 0


# --- генераторы -------------------------------------------------------------
def test_running_average() -> None:
    avg = gen.running_average()
    next(avg)
    assert [avg.send(x) for x in (2, 4, 6)] == [2, 3, 4]


def test_flatten_and_delegation() -> None:
    assert list(gen.flatten([1, [2, (3, [4])], "ab"])) == [1, 2, 3, 4, "ab"]
    g = gen.delegator(["x"])
    assert next(g) == "X"
    with pytest.raises(StopIteration) as exc:
        next(g)
    assert exc.value.value == "обработано 1"


def test_log_pipeline() -> None:
    lines = ["ERROR a: x", "INFO a: y", "ERROR b: z", "мусор"]
    assert gen.errors_per_service(lines) == {"a": 1, "b": 1}


def test_merge_files(tmp_path: Path) -> None:
    files = []
    for i in range(3):
        f = tmp_path / f"{i}.txt"
        f.write_text(f"line{i}\n", encoding="utf-8")
        files.append(f)
    out = tmp_path / "out.txt"
    assert gen.merge_files(files, out) == 3
    assert out.read_text(encoding="utf-8") == "line0\nline1\nline2\n"


def test_transaction_commit_and_rollback() -> None:
    log: list[str] = []
    with gen.transaction(log):
        pass
    with pytest.raises(KeyError), gen.transaction(log):
        raise KeyError
    assert log == ["BEGIN", "COMMIT", "BEGIN", "ROLLBACK"]


# --- паттерны -----------------------------------------------------------------
def test_result_and_match() -> None:
    assert patterns.describe(patterns.safe_divide(1, 0)) == "ошибка: деление на ноль"
    assert patterns.describe(patterns.safe_divide(6, 3)) == "результат: 2.0"


def test_registration_service_with_fakes() -> None:
    notifier = patterns.FakeNotifier()
    svc = patterns.RegistrationService(patterns.InMemoryUserRepo(), notifier)
    assert isinstance(svc.register(1, "a@b.ru"), patterns.Ok)
    assert svc.register(1, "a@b.ru") == patterns.Err("пользователь уже существует")
    assert svc.register(2, "плохой") == patterns.Err("некорректный email")
    assert notifier.sent == [("a@b.ru", "Добро пожаловать!")]


def test_singledispatch_to_json() -> None:
    import json

    data = {"a": [1, 2.5, True, None, 'q"'], "b": {"c": False}}
    assert json.loads(patterns.to_json(data)) == data
    with pytest.raises(TypeError):
        patterns.to_json(object())


def test_circuit_breaker() -> None:
    now = [0.0]
    cb = patterns.CircuitBreaker(failure_threshold=2, reset_timeout=10, clock=lambda: now[0])

    def boom() -> None:
        raise ConnectionError

    for _ in range(2):
        with pytest.raises(ConnectionError):
            cb.call(boom)
    assert cb.state == "open"
    with pytest.raises(patterns.CircuitOpenError):
        cb.call(lambda: 1)
    now[0] = 11
    assert cb.state == "half-open"
    assert cb.call(lambda: 42) == 42
    assert cb.state == "closed"


def test_event_bus() -> None:
    bus = patterns.EventBus()
    got: list[int] = []
    bus.subscribe(patterns.OrderPlaced)(lambda e: got.append(e.order_id))
    bus.subscribe(object)(lambda e: got.append(-1))  # подписка на всё
    assert bus.publish(patterns.OrderPlaced(7, 100)) == 2
    assert got == [7, -1]


# --- Python 3.14 -------------------------------------------------------------
@pytest.mark.skipif(sys.version_info < (3, 14), reason="нужен Python 3.14+")
def test_template_strings() -> None:
    ns = python314.load()
    Template = ns["Template"]
    Interpolation = ns["Interpolation"]
    evil = "<b>"
    tpl = Template("<p>", Interpolation(evil, "evil"), "</p>")
    assert ns["html"](tpl) == "<p>&lt;b&gt;</p>"
    query, params = ns["sql"](Template("id = ", Interpolation(5, "x")))
    assert (query, params) == ("id = ?", [5])
    assert ns["parse_int"]("x") is None
