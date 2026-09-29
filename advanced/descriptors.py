"""Дескрипторы: как работают property, методы и валидация полей.

Запуск: python -m advanced.descriptors
"""

from __future__ import annotations

from typing import Any, Callable


class Validated:
    """Дескриптор данных с валидацией.

    __set_name__ (Python 3.6+) сам узнаёт имя атрибута, поэтому
    не нужно писать `name = Validated("name")`.
    """

    def __init__(self, validator: Callable[[Any], bool], message: str) -> None:
        self.validator = validator
        self.message = message
        self.private_name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, instance: object | None, owner: type | None = None) -> Any:
        if instance is None:  # доступ через класс: User.age
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: Any) -> None:
        if not self.validator(value):
            raise ValueError(f"{self.public_name}: {self.message} (получено {value!r})")
        setattr(instance, self.private_name, value)


class Positive(Validated):
    def __init__(self) -> None:
        super().__init__(lambda v: isinstance(v, (int, float)) and v > 0, "должно быть > 0")


class NonEmptyStr(Validated):
    def __init__(self) -> None:
        super().__init__(lambda v: isinstance(v, str) and v.strip() != "", "непустая строка")


class Product:
    name = NonEmptyStr()
    price = Positive()
    quantity = Positive()

    def __init__(self, name: str, price: float, quantity: int) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity

    @property
    def total(self) -> float:  # property — тоже дескриптор
        return self.price * self.quantity


class lazy:  # noqa: N801 — стилизовано под встроенные декораторы
    """Дескриптор без __set__ (non-data descriptor).

    После первого вычисления значение кладётся в __dict__ экземпляра,
    и дальше Python находит его там, минуя дескриптор. Так устроен
    functools.cached_property.
    """

    def __init__(self, func: Callable[[Any], Any]) -> None:
        self.func = func
        self.__doc__ = func.__doc__

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object | None, owner: type | None = None) -> Any:
        if instance is None:
            return self
        value = self.func(instance)
        instance.__dict__[self.name] = value
        return value


class Report:
    calls = 0

    @lazy
    def data(self) -> list[int]:
        Report.calls += 1
        return [i * i for i in range(5)]


def main() -> None:
    p = Product("Ноутбук", 99_990, 2)
    print(p.name, p.total)
    try:
        p.price = -1
    except ValueError as e:
        print("Ошибка:", e)

    r = Report()
    r.data
    r.data
    print("Вычислений:", Report.calls)  # 1


if __name__ == "__main__":
    main()
