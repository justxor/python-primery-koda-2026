"""Продвинутая типизация: PEP 695, Protocol, ParamSpec, overload, TypedDict, TypeIs.

Требуется Python 3.12+ (синтаксис `def f[T]` и `type X = ...`).
Проверка: `mypy advanced/` или `pyright advanced/`.

Запуск: python -m advanced.typing_advanced
"""

from __future__ import annotations

import functools
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from typing import (
    Literal,
    NotRequired,
    Protocol,
    Required,
    Self,
    TypedDict,
    overload,
    runtime_checkable,
)

try:  # TypeIs появился в 3.13
    from typing import TypeIs
except ImportError:  # pragma: no cover — Python 3.12
    try:
        from typing_extensions import TypeIs  # type: ignore[assignment]
    except ImportError:
        from typing import TypeGuard as TypeIs  # type: ignore[assignment]


# --- 1. Дженерики нового синтаксиса (PEP 695) -------------------------------
type JSON = dict[str, JSON] | list[JSON] | str | int | float | bool | None
type Pair[T] = tuple[T, T]


def first[T](items: Iterable[T], default: T) -> T:
    return next(iter(items), default)


def clamp[N: (int, float)](value: N, lo: N, hi: N) -> N:  # ограничение типа
    return max(lo, min(value, hi))


class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> Self:  # Self — для цепочек вызовов
        self._items.append(item)
        return self

    def pop(self) -> T:
        return self._items.pop()

    def __iter__(self) -> Iterator[T]:
        return reversed(self._items)

    def __len__(self) -> int:
        return len(self._items)


# --- 2. Protocol: структурная (утиная) типизация -----------------------------
@runtime_checkable
class SupportsClose(Protocol):
    def close(self) -> None: ...


class Comparable(Protocol):
    def __lt__(self, other: Self, /) -> bool: ...


def max_item[C: Comparable](items: Iterable[C]) -> C:
    it = iter(items)
    best = next(it)
    for x in it:
        if best < x:
            best = x
    return best


class Connection:  # не наследуется от SupportsClose, но подходит
    closed = False

    def close(self) -> None:
        self.closed = True


def close_all(resources: Iterable[SupportsClose]) -> int:
    count = 0
    for r in resources:
        r.close()
        count += 1
    return count


# --- 3. ParamSpec: декоратор, сохраняющий сигнатуру ------------------------
def logged[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        wrapper.calls += 1  # type: ignore[attr-defined]
        return func(*args, **kwargs)

    wrapper.calls = 0  # type: ignore[attr-defined]
    return wrapper


@logged
def greet(name: str, *, excited: bool = False) -> str:
    return f"Привет, {name}{'!' if excited else '.'}"


# --- 4. overload: разный тип результата в зависимости от аргументов ---------
@overload
def parse(value: str, as_type: Literal["int"]) -> int: ...
@overload
def parse(value: str, as_type: Literal["float"]) -> float: ...
@overload
def parse(value: str, as_type: Literal["bool"]) -> bool: ...
def parse(value: str, as_type: str) -> int | float | bool:
    match as_type:
        case "int":
            return int(value)
        case "float":
            return float(value)
        case "bool":
            return value.strip().lower() in {"1", "true", "да", "yes"}
    raise ValueError(as_type)


# --- 5. TypedDict с Required / NotRequired -----------------------------------
class UserPayload(TypedDict, total=False):
    id: Required[int]
    name: Required[str]
    email: NotRequired[str]


def display(user: UserPayload) -> str:
    return f"#{user['id']} {user['name']} <{user.get('email', '—')}>"


# --- 6. TypeIs: пользовательские сужения типа (PEP 742) ----------------------
@dataclass
class Cat:
    name: str

    def meow(self) -> str:
        return f"{self.name}: мяу"


@dataclass
class Dog:
    name: str


def is_cat(animal: Cat | Dog) -> TypeIs[Cat]:
    return isinstance(animal, Cat)


def voices(animals: list[Cat | Dog]) -> list[str]:
    return [a.meow() for a in animals if is_cat(a)]  # тайпчекер знает, что a: Cat


def main() -> None:
    print(first([], default=0), clamp(15, 0, 10))
    s = Stack[int]().push(1).push(2).push(3)
    print(list(s), max_item([3, 9, 4]))
    print(close_all([Connection(), Connection()]), isinstance(Connection(), SupportsClose))
    print(greet("Аня", excited=True), greet.calls)  # type: ignore[attr-defined]
    print(parse("42", "int") + 1, parse("да", "bool"))
    print(display({"id": 1, "name": "Олег"}))
    print(voices([Cat("Мурка"), Dog("Шарик")]))


if __name__ == "__main__":
    main()
