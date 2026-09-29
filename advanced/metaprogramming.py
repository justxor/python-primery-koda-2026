"""Метапрограммирование: __init_subclass__, метаклассы, декораторы классов.

Правило 2026 года: сначала попробуйте декоратор класса или __init_subclass__,
метакласс — только если без него действительно нельзя.

Запуск: python -m advanced.metaprogramming
"""

from __future__ import annotations

import functools
import time
from typing import Any, ClassVar


# --- 1. Реестр плагинов через __init_subclass__ -----------------------------
class Exporter:
    registry: ClassVar[dict[str, type[Exporter]]] = {}
    fmt: ClassVar[str]

    def __init_subclass__(cls, /, fmt: str, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if fmt in Exporter.registry:
            raise TypeError(f"Формат {fmt!r} уже зарегистрирован")
        cls.fmt = fmt
        Exporter.registry[fmt] = cls

    def export(self, data: dict[str, Any]) -> str:
        raise NotImplementedError

    @classmethod
    def for_format(cls, fmt: str) -> Exporter:
        try:
            return cls.registry[fmt]()
        except KeyError:
            raise ValueError(f"Неизвестный формат: {fmt}") from None


class JsonExporter(Exporter, fmt="json"):
    def export(self, data: dict[str, Any]) -> str:
        import json

        return json.dumps(data, ensure_ascii=False)


class CsvExporter(Exporter, fmt="csv"):
    def export(self, data: dict[str, Any]) -> str:
        return ",".join(data) + "\n" + ",".join(map(str, data.values()))


# --- 2. Метакласс: синглтон ---------------------------------------------------
class SingletonMeta(type):
    _instances: ClassVar[dict[type, Any]] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in SingletonMeta._instances:
            SingletonMeta._instances[cls] = super().__call__(*args, **kwargs)
        return SingletonMeta._instances[cls]


class Settings(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.debug = False


# --- 3. Декоратор класса: замер времени всех публичных методов ---------------
def timed_methods(cls: type) -> type:
    for name, attr in list(vars(cls).items()):
        if callable(attr) and not name.startswith("_"):
            setattr(cls, name, _timed(attr))
    return cls


def _timed(func: Any) -> Any:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            wrapper.last_duration = time.perf_counter() - start  # type: ignore[attr-defined]

    wrapper.last_duration = 0.0  # type: ignore[attr-defined]
    return wrapper


@timed_methods
class Service:
    def work(self, n: int) -> int:
        return sum(range(n))


# --- 4. Динамическое создание класса через type() ----------------------------
def make_record(name: str, *fields: str) -> type:
    def __init__(self: Any, *values: Any) -> None:
        if len(values) != len(fields):
            raise TypeError(f"Ожидалось {len(fields)} значений")
        for f, v in zip(fields, values, strict=True):
            setattr(self, f, v)

    def __repr__(self: Any) -> str:
        args = ", ".join(f"{f}={getattr(self, f)!r}" for f in fields)
        return f"{name}({args})"

    return type(name, (), {"__init__": __init__, "__repr__": __repr__, "__slots__": fields})


def main() -> None:
    print(sorted(Exporter.registry))
    print(Exporter.for_format("json").export({"город": "Москва", "t": 12}))
    print(Settings() is Settings())
    s = Service()
    s.work(1_000_000)
    print(f"work: {Service.work.last_duration:.4f} с")
    Point = make_record("Point", "x", "y")
    print(Point(1, 2))


if __name__ == "__main__":
    main()
