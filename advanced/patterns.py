"""Архитектурные паттерны в современном Python.

Result-тип + match, внедрение зависимостей через Protocol, singledispatch,
Circuit Breaker и шина событий.

Запуск: python -m advanced.patterns
"""

from __future__ import annotations

import time
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import singledispatch
from typing import Protocol


# --- 1. Result: ошибки как значения + match/case -----------------------------
@dataclass(frozen=True, slots=True)
class Ok[T]:
    value: T


@dataclass(frozen=True, slots=True)
class Err[E]:
    error: E


type Result[T, E] = Ok[T] | Err[E]


def safe_divide(a: float, b: float) -> Result[float, str]:
    return Err("деление на ноль") if b == 0 else Ok(a / b)


def describe(result: Result[float, str]) -> str:
    match result:
        case Ok(value) if value < 0:
            return f"отрицательное: {value}"
        case Ok(value):
            return f"результат: {value}"
        case Err(error):
            return f"ошибка: {error}"


# --- 2. Внедрение зависимостей через Protocol --------------------------------
@dataclass
class User:
    id: int
    email: str


class UserRepository(Protocol):
    def get(self, user_id: int) -> User | None: ...
    def add(self, user: User) -> None: ...


class Notifier(Protocol):
    def send(self, to: str, text: str) -> None: ...


class InMemoryUserRepo:
    def __init__(self) -> None:
        self._data: dict[int, User] = {}

    def get(self, user_id: int) -> User | None:
        return self._data.get(user_id)

    def add(self, user: User) -> None:
        self._data[user.id] = user


@dataclass
class FakeNotifier:
    sent: list[tuple[str, str]] = field(default_factory=list)

    def send(self, to: str, text: str) -> None:
        self.sent.append((to, text))


class RegistrationService:
    """Бизнес-логика не знает про БД и SMTP — только про интерфейсы.
    В тестах подставляем фейки, в проде — настоящие реализации."""

    def __init__(self, repo: UserRepository, notifier: Notifier) -> None:
        self.repo = repo
        self.notifier = notifier

    def register(self, user_id: int, email: str) -> Result[User, str]:
        if self.repo.get(user_id):
            return Err("пользователь уже существует")
        if "@" not in email:
            return Err("некорректный email")
        user = User(user_id, email)
        self.repo.add(user)
        self.notifier.send(email, "Добро пожаловать!")
        return Ok(user)


# --- 3. singledispatch: перегрузка функции по типу аргумента -----------------
@singledispatch
def to_json(obj: object) -> str:
    raise TypeError(f"Не умею сериализовать {type(obj).__name__}")


@to_json.register
def _str(obj: str) -> str:
    return '"' + obj.replace('"', '\\"') + '"'


@to_json.register(int)
@to_json.register(float)
def _number(obj: int | float) -> str:
    return repr(obj)


@to_json.register
def _bool(obj: bool) -> str:  # bool — подкласс int, но выбирается точнее
    return "true" if obj else "false"


@to_json.register(type(None))
def _none(obj: None) -> str:
    return "null"


@to_json.register
def _list(obj: list) -> str:
    return "[" + ",".join(map(to_json, obj)) + "]"


@to_json.register
def _dict(obj: dict) -> str:
    return "{" + ",".join(f"{to_json(str(k))}:{to_json(v)}" for k, v in obj.items()) + "}"


# --- 4. Circuit Breaker: не долбим упавший сервис ----------------------------
class CircuitOpenError(RuntimeError):
    pass


class CircuitBreaker:
    """closed → (N ошибок) → open → (таймаут) → half-open → closed/open"""

    def __init__(
        self,
        failure_threshold: int = 3,
        reset_timeout: float = 30.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.clock = clock
        self.failures = 0
        self.opened_at: float | None = None

    @property
    def state(self) -> str:
        if self.opened_at is None:
            return "closed"
        if self.clock() - self.opened_at >= self.reset_timeout:
            return "half-open"
        return "open"

    def call[**P, R](self, func: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
        if self.state == "open":
            raise CircuitOpenError("сервис временно недоступен")
        try:
            result = func(*args, **kwargs)
        except Exception:
            self.failures += 1
            if self.state == "half-open" or self.failures >= self.failure_threshold:
                self.opened_at = self.clock()
            raise
        self.failures = 0
        self.opened_at = None
        return result


# --- 5. Шина событий (Observer) ------------------------------------------------
class EventBus:
    def __init__(self) -> None:
        self._handlers: defaultdict[type, list[Callable]] = defaultdict(list)

    def subscribe[E](self, event_type: type[E]) -> Callable[[Callable[[E], None]], Callable[[E], None]]:
        def decorator(handler: Callable[[E], None]) -> Callable[[E], None]:
            self._handlers[event_type].append(handler)
            return handler

        return decorator

    def publish(self, event: object) -> int:
        called = 0
        for cls in type(event).__mro__:  # подписчики базовых событий тоже получат
            for handler in self._handlers.get(cls, []):
                handler(event)
                called += 1
        return called


@dataclass(frozen=True)
class OrderPlaced:
    order_id: int
    total: float


def main() -> None:
    for r in (safe_divide(1, 4), safe_divide(-1, 2), safe_divide(1, 0)):
        print(describe(r))

    notifier = FakeNotifier()
    svc = RegistrationService(InMemoryUserRepo(), notifier)
    print(svc.register(1, "a@b.ru"), svc.register(1, "a@b.ru"), notifier.sent)

    print(to_json({"ok": True, "items": [1, 2.5, None, "x"]}))

    bus = EventBus()

    @bus.subscribe(OrderPlaced)
    def send_receipt(e: OrderPlaced) -> None:
        print(f"Чек по заказу #{e.order_id} на {e.total} ₽")

    bus.publish(OrderPlaced(42, 1990.0))


if __name__ == "__main__":
    main()
