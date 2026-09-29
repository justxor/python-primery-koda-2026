# Примеры кода на Python 2026: лучшие практики, разбор и задачи с решениями

> **Python примеры кода 2026** — практическое руководство на русском языке: разбор лучших примеров кода на Python, современные паттерны Python 3.12–3.14, чистый код, асинхронность, типизация, тестирование и задачи для практики с решениями. Подходит для начинающих, junior-, middle- и senior-разработчиков, а также для подготовки к собеседованию по Python.

![Python](https://img.shields.io/badge/Python-3.12%20|%203.13%20|%203.14-blue)
![Язык](https://img.shields.io/badge/язык-русский-red)
![Уровень](https://img.shields.io/badge/уровень-от%20новичка%20до%20senior-green)
![Лицензия](https://img.shields.io/badge/лицензия-MIT-lightgrey)
![Tests](https://github.com/justxor/python-primery-koda-2026/actions/workflows/tests.yml/badge.svg)

**Ключевые темы:** примеры кода Python, лучшие практики Python 2026, python для начинающих, задачи по Python с решениями, чистый код на Python, асинхронный Python, asyncio примеры, типизация в Python, pytest примеры, FastAPI пример, парсинг на Python, подготовка к собеседованию Python, Python 3.14 новые возможности, дескрипторы, метаклассы, contextvars, free-threaded Python, t-строки, паттерны проектирования на Python.

---

## Полезные каналы

🖥 **Pythonl** ([канал 1](https://t.me/+p-hGlzVQrqM4MDI6), [канал 2](https://t.me/+DNiTvr30y9BiNzli)) — с помощью понятных картинок и коротких видео авторы объясняют сложные концепции и учат профессиональному подходу в разработке.

🖥 [**Python Интервью**](https://t.me/+sTT6sbZubDM2MWEy) — огромное количество разобранных вопросов с реальных собеседований Python-разработчика.

🧠 **Machine learning** ([канал 1](https://t.me/+pQPz7SU6PMpjODNi), [канал 2](https://t.me/+rn-i1Uz1lDtjNmFi)) — ИИ-инструменты для генерации Python-кода, умные агенты и всё, что нужно знать из области AI.

🔝 [**А здесь мы собрали**](https://t.me/addlist/8vDUwYRGujRmZjFi) целый кладезь полезных Python-ресурсов для прокачки.

---

## Содержание

1. [Почему Python в 2026 году](#почему-python-в-2026-году)
2. [Современный стек Python-разработчика 2026](#современный-стек-python-разработчика-2026)
3. [Разбор лучших примеров кода на Python](#разбор-лучших-примеров-кода-на-python)
   - [Чистый и идиоматичный код](#1-чистый-и-идиоматичный-код-pythonic-way)
   - [Типизация: аннотации типов и дженерики](#2-типизация-аннотации-типов-и-дженерики)
   - [Dataclasses и Pydantic](#3-dataclasses-и-pydantic-модели-данных)
   - [Сопоставление с образцом (match/case)](#4-сопоставление-с-образцом-matchcase)
   - [Асинхронность: asyncio и TaskGroup](#5-асинхронность-asyncio-и-taskgroup)
   - [Работа с файлами через pathlib](#6-работа-с-файлами-через-pathlib)
   - [Обработка ошибок и ExceptionGroup](#7-обработка-ошибок-и-exceptiongroup)
   - [Контекстные менеджеры и декораторы](#8-контекстные-менеджеры-и-декораторы)
   - [Генераторы и itertools](#9-генераторы-и-itertools)
   - [Логирование вместо print](#10-логирование-вместо-print)
4. [Продвинутые темы Python (middle+ / senior)](#продвинутые-темы-python-middle--senior)
   - [Дескрипторы](#11-дескрипторы-как-устроены-property-и-валидация-полей)
   - [Метапрограммирование: `__init_subclass__` и метаклассы](#12-метапрограммирование-__init_subclass__-и-метаклассы)
   - [Продвинутая типизация: PEP 695, Protocol, ParamSpec](#13-продвинутая-типизация-pep-695-protocol-paramspec-typeis)
   - [Паттерны asyncio: семафоры, очереди, retry, отмена](#14-паттерны-asyncio-семафоры-очереди-retry-отмена)
   - [Параллелизм: GIL, free-threading, субинтерпретаторы](#15-параллелизм-gil-free-threading-субинтерпретаторы)
   - [contextvars: контекст запроса в асинхронном коде](#16-contextvars-контекст-запроса-в-асинхронном-коде)
   - [Производительность и память](#17-производительность-и-память-__slots__-weakref-профилирование)
   - [Продвинутые генераторы и ExitStack](#18-продвинутые-генераторы-send-yield-from-exitstack)
   - [Паттерны: Result, DI, Circuit Breaker](#19-архитектурные-паттерны-result-di-circuit-breaker)
   - [Python 3.14 в коде: t-строки и annotationlib](#20-python-314-в-коде-t-строки-annotationlib-except-без-скобок)
5. [Что нового в Python 3.13 и 3.14](#что-нового-в-python-313-и-314)
6. [Практика: задачи по Python с решениями](#практика-задачи-по-python-с-решениями)
7. [Мини-проекты для портфолио](#мини-проекты-для-портфолио)
8. [Тестирование: pytest примеры](#тестирование-pytest-примеры)
9. [Частые ошибки новичков в Python](#частые-ошибки-новичков-в-python)
10. [Вопросы с собеседований по Python](#вопросы-с-собеседований-по-python)
11. [FAQ](#faq--частые-вопросы)
12. [Полезные ресурсы](#полезные-ресурсы)

---

## Почему Python в 2026 году

Python остаётся одним из самых популярных языков программирования в мире. Его используют для:

- **веб-разработки** — FastAPI, Django, Litestar;
- **анализа данных** — pandas, Polars, DuckDB;
- **машинного обучения и ИИ** — PyTorch, scikit-learn, Transformers, LLM-агенты;
- **автоматизации и скриптов** — парсинг, боты, DevOps-утилиты;
- **научных вычислений** — NumPy, SciPy, Jupyter.

В 2026 году экосистема Python стала быстрее и удобнее: менеджер пакетов **uv**, линтер **Ruff**, экспериментальный режим без GIL (free-threaded Python), улучшенный интерпретатор и сообщения об ошибках.

---

## Современный стек Python-разработчика 2026

| Задача | Инструмент | Зачем |
|---|---|---|
| Управление версиями и зависимостями | `uv` | Быстрая замена pip, venv, pip-tools и pyenv |
| Линтинг и форматирование | `ruff` | Заменяет flake8, isort, black в одном инструменте |
| Проверка типов | `mypy`, `pyright` | Находит ошибки до запуска |
| Тесты | `pytest` | Стандарт де-факто для тестирования |
| Веб-API | `FastAPI` | Асинхронный, с автодокументацией OpenAPI |
| Валидация данных | `pydantic` v2 | Быстрая валидация на основе типов |
| HTTP-клиент | `httpx` | Синхронный и асинхронный клиент |
| Таблицы и данные | `polars`, `pandas` | Обработка табличных данных |
| Pre-commit хуки | `pre-commit` | Автопроверки перед коммитом |

### Быстрый старт проекта с uv

```bash
# установка uv (Linux/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh

# новый проект
uv init my-project
cd my-project

# добавить зависимости
uv add httpx pydantic
uv add --dev pytest ruff mypy

# запуск
uv run main.py
uv run pytest
```

### Минимальный `pyproject.toml` с Ruff

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["httpx", "pydantic"]

[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]
```

---

## Разбор лучших примеров кода на Python

Каждый пример построен по схеме: **плохо → хорошо → почему**.

### 1. Чистый и идиоматичный код (Pythonic way)

**Плохо:**

```python
result = []
for i in range(len(users)):
    if users[i]["active"] == True:
        result.append(users[i]["name"].upper())
```

**Хорошо:**

```python
active_names = [user["name"].upper() for user in users if user["active"]]
```

**Почему:** list comprehension короче и быстрее, итерация идёт по элементам, а не по индексам, сравнение с `True` избыточно.

**Ещё идиомы, которые стоит знать:**

```python
# enumerate вместо счётчика
for index, item in enumerate(items, start=1):
    print(f"{index}. {item}")

# zip для параллельного обхода (strict=True ловит разную длину)
for name, score in zip(names, scores, strict=True):
    print(f"{name}: {score}")

# распаковка
first, *middle, last = [1, 2, 3, 4, 5]

# словарь со значением по умолчанию
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

# ещё лучше — Counter
from collections import Counter
top = Counter(words).most_common(3)

# walrus-оператор :=
if (n := len(data)) > 100:
    print(f"Слишком много данных: {n}")

# объединение словарей
config = defaults | user_settings
```

---

### 2. Типизация: аннотации типов и дженерики

Начиная с Python 3.12 дженерики объявляются новым синтаксисом (PEP 695), а псевдонимы типов — через `type`.

```python
from collections.abc import Iterable, Callable

type UserId = int
type JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


def first[T](items: Iterable[T], default: T | None = None) -> T | None:
    """Вернуть первый элемент или значение по умолчанию."""
    return next(iter(items), default)


class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("стек пуст")
        return self._items.pop()


def apply_twice[T](func: Callable[[T], T], value: T) -> T:
    return func(func(value))
```

**Почему:** типы — это документация, которая проверяется автоматически (`mypy`, `pyright`) и даёт точное автодополнение в IDE.

---

### 3. Dataclasses и Pydantic: модели данных

**Dataclass** — для внутренних структур:

```python
from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class Product:
    name: str
    price: float
    tags: list[str] = field(default_factory=list)

    @property
    def price_with_vat(self) -> float:
        return round(self.price * 1.2, 2)


p = Product("Клавиатура", 3500)
print(p.price_with_vat)  # 4200.0
```

**Pydantic** — для данных извне (API, JSON, конфиги):

```python
from pydantic import BaseModel, EmailStr, Field


class UserIn(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(ge=0, le=150)


user = UserIn.model_validate({"name": "Анна", "email": "anna@example.com", "age": 28})
print(user.model_dump_json())
```

> Для `EmailStr` установите `pydantic[email]`.

**Правило:** `dataclass` — внутри приложения, `pydantic` — на границе с внешним миром.

---

### 4. Сопоставление с образцом (match/case)

```python
def handle(event: dict) -> str:
    match event:
        case {"type": "click", "x": int(x), "y": int(y)}:
            return f"Клик в точке ({x}, {y})"
        case {"type": "key", "key": "Enter" | "Return"}:
            return "Нажат Enter"
        case {"type": "key", "key": str(key)}:
            return f"Клавиша {key}"
        case {"type": t}:
            return f"Неизвестное событие: {t}"
        case _:
            return "Некорректные данные"


print(handle({"type": "click", "x": 10, "y": 20}))
```

**Почему:** `match/case` заменяет длинные цепочки `if/elif` и одновременно проверяет структуру и извлекает значения.

---

### 5. Асинхронность: asyncio и TaskGroup

Параллельная загрузка страниц через `httpx` и `asyncio.TaskGroup` (Python 3.11+):

```python
import asyncio
import httpx

URLS = [
    "https://www.python.org",
    "https://docs.python.org/3/",
    "https://pypi.org",
]


async def fetch(client: httpx.AsyncClient, url: str) -> tuple[str, int]:
    response = await client.get(url, follow_redirects=True)
    return url, response.status_code


async def main() -> None:
    async with httpx.AsyncClient(timeout=10) as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(fetch(client, url)) for url in URLS]

    for task in tasks:
        url, status = task.result()
        print(f"{status} — {url}")


if __name__ == "__main__":
    asyncio.run(main())
```

**Ограничение параллелизма семафором:**

```python
sem = asyncio.Semaphore(5)

async def fetch_limited(client: httpx.AsyncClient, url: str):
    async with sem:
        return await fetch(client, url)
```

**Таймаут на группу операций:**

```python
async with asyncio.timeout(5):
    await long_operation()
```

**Почему:** `TaskGroup` безопаснее `asyncio.gather` — при ошибке в одной задаче остальные отменяются, а все исключения собираются в `ExceptionGroup`.

---

### 6. Работа с файлами через pathlib

**Плохо:**

```python
import os
path = os.path.join(os.getcwd(), "data", "report.txt")
f = open(path)
text = f.read()
f.close()
```

**Хорошо:**

```python
from pathlib import Path

path = Path.cwd() / "data" / "report.txt"
text = path.read_text(encoding="utf-8")

# все CSV-файлы рекурсивно
for csv_file in Path("data").rglob("*.csv"):
    print(csv_file.name, csv_file.stat().st_size)

# создать папку, если её нет
Path("output").mkdir(parents=True, exist_ok=True)
```

**Почему:** `pathlib` кроссплатформенный, читаемый и сам закрывает файлы. Всегда указывайте `encoding="utf-8"`.

---

### 7. Обработка ошибок и ExceptionGroup

```python
class ValidationError(Exception):
    """Ошибка валидации пользовательских данных."""


def parse_age(raw: str) -> int:
    try:
        age = int(raw)
    except ValueError as exc:
        raise ValidationError(f"Возраст должен быть числом, получено: {raw!r}") from exc
    if not 0 <= age <= 150:
        raise ValidationError(f"Недопустимый возраст: {age}")
    return age
```

Обработка нескольких ошибок сразу через `except*`:

```python
try:
    raise ExceptionGroup("ошибки", [ValueError("a"), TypeError("b")])
except* ValueError as group:
    print("ValueError:", group.exceptions)
except* TypeError as group:
    print("TypeError:", group.exceptions)
```

**Правила:**
- никогда не пишите голый `except:` — он глотает даже `KeyboardInterrupt`;
- ловите конкретные исключения;
- используйте `raise ... from exc`, чтобы сохранить причину;
- создавайте свои классы исключений для бизнес-логики.

---

### 8. Контекстные менеджеры и декораторы

**Контекстный менеджер для замера времени:**

```python
import time
from contextlib import contextmanager


@contextmanager
def timer(label: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        print(f"{label}: {time.perf_counter() - start:.3f} с")


with timer("Сортировка"):
    sorted(range(1_000_000), reverse=True)
```

**Декоратор с повторными попытками (retry):**

```python
import functools
import time


def retry(times: int = 3, delay: float = 1.0, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    if attempt == times:
                        raise
                    print(f"Попытка {attempt} не удалась: {exc}. Повтор через {delay} с")
                    time.sleep(delay)
        return wrapper
    return decorator


@retry(times=3, delay=0.5, exceptions=(ConnectionError,))
def unstable_request():
    ...
```

**Кэширование результатов:**

```python
from functools import cache


@cache
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print(fib(100))
```

---

### 9. Генераторы и itertools

Генераторы обрабатывают большие данные без загрузки всего в память:

```python
from pathlib import Path


def read_large_file(path: Path):
    with path.open(encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")


errors = (line for line in read_large_file(Path("app.log")) if "ERROR" in line)
for line in errors:
    print(line)
```

Полезные функции `itertools`:

```python
from itertools import batched, chain, groupby, islice, pairwise

list(batched(range(10), 3))        # [(0,1,2), (3,4,5), (6,7,8), (9,)]  — Python 3.12+
list(pairwise([1, 2, 3, 4]))       # [(1,2), (2,3), (3,4)]
list(chain([1, 2], [3], [4, 5]))   # [1, 2, 3, 4, 5]
list(islice(range(100), 5))        # [0, 1, 2, 3, 4]

data = sorted(["apple", "avocado", "banana", "cherry"], key=lambda s: s[0])
for letter, group in groupby(data, key=lambda s: s[0]):
    print(letter, list(group))
```

---

### 10. Логирование вместо print

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


def process(order_id: int) -> None:
    logger.info("Обработка заказа %s", order_id)
    try:
        ...
    except Exception:
        logger.exception("Ошибка при обработке заказа %s", order_id)
        raise
```

**Почему:** уровни логов, время, имя модуля и трассировка ошибок — всё это `print` не умеет. Передавайте аргументы через `%s`, а не f-строкой: форматирование выполнится, только если сообщение действительно будет выведено.

---

## Продвинутые темы Python (middle+ / senior)

Полный рабочий код каждой темы лежит в папке [`advanced/`](advanced/), а тесты — в [`tests/test_advanced.py`](tests/test_advanced.py). Все примеры проверены на Python 3.12, 3.13 и 3.14 (CI в GitHub Actions).

```bash
git clone https://github.com/justxor/python-primery-koda-2026.git
cd python-primery-koda-2026
uv run python -m advanced.asyncio_patterns   # запустить любой пример
uv run --with pytest pytest                  # прогнать все тесты
```

| # | Тема | Файл | Уровень |
|---|------|------|---------|
| 11 | Дескрипторы, `__set_name__`, ленивые атрибуты | [`descriptors.py`](advanced/descriptors.py) | middle+ |
| 12 | `__init_subclass__`, метаклассы, `type()` | [`metaprogramming.py`](advanced/metaprogramming.py) | senior |
| 13 | PEP 695, `Protocol`, `ParamSpec`, `overload`, `TypeIs` | [`typing_advanced.py`](advanced/typing_advanced.py) | middle+ |
| 14 | Semaphore, Queue, retry, `timeout`, `shield` | [`asyncio_patterns.py`](advanced/asyncio_patterns.py) | middle+ |
| 15 | GIL, free-threading, `InterpreterPoolExecutor` | [`concurrency.py`](advanced/concurrency.py) | senior |
| 16 | `contextvars` и request_id в логах | [`contextvars_demo.py`](advanced/contextvars_demo.py) | middle+ |
| 17 | `__slots__`, `weakref`, `tracemalloc`, `cProfile` | [`performance.py`](advanced/performance.py) | middle+ |
| 18 | `send()`, `yield from`, конвейеры, `ExitStack` | [`generators_advanced.py`](advanced/generators_advanced.py) | middle+ |
| 19 | Result, DI, `singledispatch`, Circuit Breaker, EventBus | [`patterns.py`](advanced/patterns.py) | senior |
| 20 | t-строки, `annotationlib`, `except A, B` | [`python314.py`](advanced/python314.py) | все |

---

### 11. Дескрипторы: как устроены property и валидация полей

`property`, `classmethod`, `staticmethod` и даже обычные методы — это дескрипторы. Свой дескриптор позволяет один раз описать правило и переиспользовать его в любом классе:

```python
class Positive:
    def __set_name__(self, owner, name):        # Python сам сообщит имя атрибута
        self.name, self.private = name, f"_{name}"

    def __get__(self, instance, owner=None):
        return self if instance is None else getattr(instance, self.private)

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(f"{self.name} должно быть > 0, получено {value!r}")
        setattr(instance, self.private, value)


class Product:
    price = Positive()
    quantity = Positive()

    def __init__(self, price, quantity):
        self.price = price          # вызывает Positive.__set__
        self.quantity = quantity


Product(100, 2)
Product(-1, 2)   # ValueError: price должно быть > 0, получено -1
```

**Важно:** дескриптор с `__set__` (data descriptor) имеет приоритет над `__dict__` экземпляра, а без `__set__` — нет. На этом построен `functools.cached_property`: после первого вызова значение кладётся в `__dict__` и дескриптор больше не вызывается.

---

### 12. Метапрограммирование: `__init_subclass__` и метаклассы

В 90% случаев вместо метакласса хватает `__init_subclass__` — например, для автоматического реестра плагинов:

```python
class Exporter:
    registry: dict[str, type["Exporter"]] = {}

    def __init_subclass__(cls, /, fmt: str, **kwargs):
        super().__init_subclass__(**kwargs)
        Exporter.registry[fmt] = cls


class JsonExporter(Exporter, fmt="json"): ...
class CsvExporter(Exporter, fmt="csv"): ...

print(Exporter.registry)   # {'json': <class JsonExporter>, 'csv': <class CsvExporter>}
```

Метакласс нужен, когда надо вмешаться в сам процесс создания экземпляров или класса — например, синглтон:

```python
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Settings(metaclass=SingletonMeta): ...

assert Settings() is Settings()
```

**Порядок выбора:** декоратор класса → `__init_subclass__` → `__set_name__` → метакласс.

---

### 13. Продвинутая типизация: PEP 695, Protocol, ParamSpec, TypeIs

```python
from collections.abc import Callable
from typing import Protocol, Self
import functools

type JSON = dict[str, JSON] | list[JSON] | str | int | float | bool | None   # рекурсивный алиас


class Stack[T]:                            # дженерик-класс без TypeVar
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> Self:       # Self — для цепочек вызовов
        self._items.append(item)
        return self


class Comparable(Protocol):                # структурная типизация
    def __lt__(self, other: Self, /) -> bool: ...


def max_item[C: Comparable](items: list[C]) -> C:
    return max(items)


def logged[**P, R](func: Callable[P, R]) -> Callable[P, R]:   # ParamSpec
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print("вызов", func.__name__)
        return func(*args, **kwargs)
    return wrapper
```

Благодаря `ParamSpec` IDE и mypy видят настоящую сигнатуру задекорированной функции, а не `(*args, **kwargs)`. `TypeIs` (Python 3.13) позволяет писать собственные функции сужения типа, которые работают в обе стороны — в `if` и в `else`.

---

### 14. Паттерны asyncio: семафоры, очереди, retry, отмена

**Ограничение параллелизма** — не больше N запросов одновременно:

```python
import asyncio


async def gather_limited(coros, limit: int):
    sem = asyncio.Semaphore(limit)

    async def run(coro):
        async with sem:
            return await coro

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(run(c)) for c in coros]
    return [t.result() for t in tasks]
```

**Повтор с экспоненциальной задержкой и джиттером** (чтобы тысяча клиентов не повторяла запрос одновременно):

```python
import random


async def retry_async(func, *, attempts=5, base_delay=0.1, max_delay=5.0):
    for attempt in range(attempts):
        try:
            return await func()
        except (ConnectionError, TimeoutError):
            if attempt == attempts - 1:
                raise
            await asyncio.sleep(random.uniform(0, min(max_delay, base_delay * 2**attempt)))
```

Ещё в файле: producer/consumer на `asyncio.Queue` с backpressure, `asyncio.timeout()`, асинхронные генераторы с корректным закрытием, `asyncio.shield()` для операций, которые нельзя прерывать, и `asyncio.to_thread()` для блокирующего кода.

---

### 15. Параллелизм: GIL, free-threading, субинтерпретаторы

| Задача | Инструмент |
|--------|------------|
| I/O: сеть, диск, БД | `asyncio`, `ThreadPoolExecutor` |
| CPU: вычисления | `ProcessPoolExecutor` |
| CPU в free-threaded сборке (3.13t / 3.14t) | обычные потоки — GIL выключен |
| CPU с изоляцией, но дешевле процессов (3.14+) | `InterpreterPoolExecutor` |

```python
import sys, sysconfig
import concurrent.futures as cf

print("free-threaded:", bool(sysconfig.get_config_var("Py_GIL_DISABLED")))
print("GIL включён:", sys._is_gil_enabled())      # Python 3.13+


def best_executor() -> type[cf.Executor]:
    if not sys._is_gil_enabled():
        return cf.ThreadPoolExecutor
    if hasattr(cf, "InterpreterPoolExecutor"):    # Python 3.14+
        return cf.InterpreterPoolExecutor
    return cf.ProcessPoolExecutor
```

**Подвох:** без GIL гонки данных становятся реальностью. `counter += 1` не атомарна — защищайте общее состояние через `threading.Lock`.

---

### 16. contextvars: контекст запроса в асинхронном коде

Глобальные переменные и `threading.local` ломаются в asyncio: в одном потоке одновременно выполняются сотни запросов. `ContextVar` хранит значение отдельно для каждой задачи:

```python
from contextvars import ContextVar
import logging

request_id: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id.get()   # id запроса в каждой строке лога
        return True


async def handle(rid: str):
    token = request_id.set(rid)
    try:
        await do_work()        # глубоко внутри request_id.get() вернёт rid
    finally:
        request_id.reset(token)
```

Так работают middleware в FastAPI/Starlette, OpenTelemetry и structlog.

---

### 17. Производительность и память: `__slots__`, weakref, профилирование

```python
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Point:
    x: float
    y: float
# экземпляр без __dict__: ~48 байт вместо ~340, доступ к атрибутам быстрее
```

- **`functools.cached_property`** — вычислить один раз и запомнить на экземпляре.
- **`functools.lru_cache`** — мемоизация чистых функций, `cache_info()` показывает эффективность.
- **`weakref.WeakValueDictionary`** — кэш, который не мешает сборщику мусора удалять объекты.
- **`tracemalloc`** — где и сколько памяти выделено; **`cProfile` + `pstats`** — где тратится время.
- **`timeit`** — честное сравнение двух вариантов кода.

```bash
python -m cProfile -s cumulative script.py | head -20
python -X importtime -c "import mymodule"     # что медленно импортируется
```

**Правило:** сначала измерьте, потом оптимизируйте.

---

### 18. Продвинутые генераторы: `send()`, `yield from`, ExitStack

```python
def running_average():
    total = count = 0
    average = 0.0
    while True:
        value = yield average          # получаем значение через send()
        total += value
        count += 1
        average = total / count


avg = running_average()
next(avg)                              # «прогрев» до первого yield
avg.send(10); avg.send(20)             # 15.0
```

**Конвейер генераторов** обрабатывает лог в десятки гигабайт с постоянным потреблением памяти:

```python
errors = count_by("service", only("ERROR", parse(open("app.log"))))
```

**`ExitStack`** — когда количество контекстных менеджеров заранее неизвестно:

```python
from contextlib import ExitStack

with ExitStack() as stack:
    files = [stack.enter_context(open(p, encoding="utf-8")) for p in paths]
    ...   # все файлы гарантированно закроются
```

---

### 19. Архитектурные паттерны: Result, DI, Circuit Breaker

**Ошибки как значения** + `match/case`:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Ok[T]:
    value: T


@dataclass(frozen=True)
class Err[E]:
    error: E


type Result[T, E] = Ok[T] | Err[E]


def safe_divide(a: float, b: float) -> Result[float, str]:
    return Err("деление на ноль") if b == 0 else Ok(a / b)


match safe_divide(1, 0):
    case Ok(value):
        print("результат", value)
    case Err(error):
        print("ошибка", error)
```

**Внедрение зависимостей через `Protocol`:** бизнес-логика зависит от интерфейса `UserRepository`, а не от PostgreSQL. В тестах подставляется `InMemoryUserRepo` — без моков и `patch`.

**Circuit Breaker** — после N ошибок подряд перестаём обращаться к упавшему сервису на время `reset_timeout`, затем пробуем снова (состояния closed → open → half-open). Полная реализация и тесты с подменой часов — в [`patterns.py`](advanced/patterns.py).

---

### 20. Python 3.14 в коде: t-строки, annotationlib, except без скобок

**t-строки (PEP 750)** выглядят как f-строки, но возвращают объект `Template`, а не готовую строку. Это позволяет безопасно обработать подстановки — например, экранировать HTML или превратить запрос в параметризованный SQL:

```python
from string.templatelib import Interpolation, Template


def sql(template: Template) -> tuple[str, list]:
    query, params = [], []
    for part in template:
        if isinstance(part, Interpolation):
            query.append("?")
            params.append(part.value)
        else:
            query.append(part)
    return "".join(query), params


name = "Robert'); DROP TABLE students;--"
sql(t"SELECT * FROM users WHERE name = {name}")
# ('SELECT * FROM users WHERE name = ?', ["Robert'); DROP TABLE students;--"])
```

**Отложенные аннотации (PEP 649):** можно ссылаться на класс, объявленный ниже, без кавычек и `from __future__ import annotations`; читать аннотации — через `annotationlib.get_annotations()`.

**PEP 758:** `except ValueError, TypeError:` — скобки больше не обязательны (если нет `as`).

---

## Что нового в Python 3.13 и 3.14

**Python 3.13:**
- новый интерактивный REPL с подсветкой и многострочным редактированием;
- экспериментальная сборка **без GIL** (free-threaded, PEP 703);
- экспериментальный JIT-компилятор (PEP 744);
- более понятные и цветные сообщения об ошибках.

**Python 3.14:**
- **t-строки** (template strings, PEP 750) — шаблоны для безопасной подстановки, например в SQL и HTML;
- отложенное вычисление аннотаций (PEP 649/749) и модуль `annotationlib`;
- `except` и `except*` без скобок при перечислении нескольких исключений (PEP 758);
- несколько интерпретаторов в одном процессе — `concurrent.interpreters` (PEP 734);
- модуль `compression.zstd` для сжатия Zstandard (PEP 784);
- free-threaded сборка получила официальную поддержку (PEP 779).

Пример t-строки (Python 3.14):

```python
from string.templatelib import Template

name = "<script>alert(1)</script>"
template: Template = t"Привет, {name}!"

print(template.strings)                     # ('Привет, ', '!')
print([i.value for i in template.interpolations])  # ['<script>alert(1)</script>']
```

Пример `except` без скобок (Python 3.14):

```python
try:
    connect()
except TimeoutError, ConnectionRefusedError:
    print("Сервер недоступен")
```

---

## Практика: задачи по Python с решениями

Попробуйте решить задачу самостоятельно, а затем откройте решение.

### Задача 1. Палиндром (уровень: новичок)

Напишите функцию, которая проверяет, является ли строка палиндромом без учёта регистра, пробелов и знаков препинания.

<details>
<summary>Решение</summary>

```python
def is_palindrome(text: str) -> bool:
    cleaned = [ch.lower() for ch in text if ch.isalnum()]
    return cleaned == cleaned[::-1]


assert is_palindrome("А роза упала на лапу Азора")
assert not is_palindrome("Python")
```
</details>

### Задача 2. Частота слов (уровень: новичок)

Найдите 5 самых частых слов в тексте.

<details>
<summary>Решение</summary>

```python
import re
from collections import Counter


def top_words(text: str, n: int = 5) -> list[tuple[str, int]]:
    words = re.findall(r"\w+", text.lower())
    return Counter(words).most_common(n)
```
</details>

### Задача 3. Группировка анаграмм (уровень: junior)

Сгруппируйте слова-анаграммы: `["кот", "ток", "сон", "нос", "кит"]`.

<details>
<summary>Решение</summary>

```python
from collections import defaultdict


def group_anagrams(words: list[str]) -> list[list[str]]:
    groups: defaultdict[str, list[str]] = defaultdict(list)
    for word in words:
        groups["".join(sorted(word))].append(word)
    return list(groups.values())


print(group_anagrams(["кот", "ток", "сон", "нос", "кит"]))
# [['кот', 'ток'], ['сон', 'нос'], ['кит']]
```
</details>

### Задача 4. Проверка скобок (уровень: junior)

Проверьте, правильно ли расставлены скобки `()[]{}` в строке.

<details>
<summary>Решение</summary>

```python
def is_balanced(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


assert is_balanced("{[()()]}")
assert not is_balanced("([)]")
```
</details>

### Задача 5. LRU-кэш (уровень: middle)

Реализуйте кэш фиксированного размера, вытесняющий давно неиспользуемые элементы.

<details>
<summary>Решение</summary>

```python
from collections import OrderedDict


class LRUCache[K, V]:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._data: OrderedDict[K, V] = OrderedDict()

    def get(self, key: K) -> V | None:
        if key not in self._data:
            return None
        self._data.move_to_end(key)
        return self._data[key]

    def put(self, key: K, value: V) -> None:
        self._data[key] = value
        self._data.move_to_end(key)
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)


cache = LRUCache[str, int](2)
cache.put("a", 1)
cache.put("b", 2)
cache.get("a")
cache.put("c", 3)       # вытесняет "b"
assert cache.get("b") is None
```
</details>

### Задача 6. Асинхронный rate limiter (уровень: middle)

Выполните 20 асинхронных задач, но не более 5 одновременно.

<details>
<summary>Решение</summary>

```python
import asyncio
import random


async def job(i: int, sem: asyncio.Semaphore) -> int:
    async with sem:
        await asyncio.sleep(random.uniform(0.1, 0.5))
        return i * i


async def main() -> None:
    sem = asyncio.Semaphore(5)
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(job(i, sem)) for i in range(20)]
    print([t.result() for t in tasks])


asyncio.run(main())
```
</details>

### Задача 7. Плоский список (уровень: junior)

Превратите произвольно вложенный список в плоский: `[1, [2, [3, [4]], 5]] → [1, 2, 3, 4, 5]`.

<details>
<summary>Решение</summary>

```python
from collections.abc import Iterable, Iterator


def flatten(items: Iterable) -> Iterator:
    for item in items:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            yield from flatten(item)
        else:
            yield item


assert list(flatten([1, [2, [3, [4]], 5]])) == [1, 2, 3, 4, 5]
```
</details>

---

## Мини-проекты для портфолио

| Проект | Что изучите | Стек |
|---|---|---|
| Консольный менеджер задач | CLI, файлы, JSON | `argparse`, `pathlib`, `json` |
| Telegram-бот | асинхронность, API | `aiogram` |
| REST API для заметок | веб, БД, валидация | `FastAPI`, `SQLAlchemy`, `pydantic` |
| Парсер цен | HTTP, HTML, расписание | `httpx`, `selectolax` / `BeautifulSoup` |
| Дашборд по данным | анализ и визуализация | `polars`, `streamlit` |
| LLM-ассистент | работа с API нейросетей | SDK провайдера, `pydantic` |

### Пример: REST API на FastAPI за 30 строк

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Заметки API")


class NoteIn(BaseModel):
    title: str
    text: str = ""


class Note(NoteIn):
    id: int


notes: dict[int, Note] = {}


@app.post("/notes", response_model=Note, status_code=201)
def create_note(data: NoteIn) -> Note:
    note = Note(id=len(notes) + 1, **data.model_dump())
    notes[note.id] = note
    return note


@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int) -> Note:
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    return notes[note_id]
```

Запуск: `uv add "fastapi[standard]"` и `uv run fastapi dev main.py`, документация — на `http://127.0.0.1:8000/docs`.

---

## Тестирование: pytest примеры

```python
# test_utils.py
import pytest
from utils import is_palindrome, is_balanced


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("шалаш", True),
        ("А роза упала на лапу Азора", True),
        ("python", False),
        ("", True),
    ],
)
def test_is_palindrome(text: str, expected: bool) -> None:
    assert is_palindrome(text) is expected


def test_is_balanced_empty_string() -> None:
    assert is_balanced("")


@pytest.fixture
def sample_users() -> list[dict]:
    return [{"name": "Анна", "active": True}, {"name": "Борис", "active": False}]


def test_active_users(sample_users: list[dict]) -> None:
    active = [u["name"] for u in sample_users if u["active"]]
    assert active == ["Анна"]
```

Запуск: `uv run pytest -v`.

---

## Частые ошибки новичков в Python

1. **Изменяемый аргумент по умолчанию**

   ```python
   # плохо
   def add(item, bucket=[]):
       bucket.append(item)
       return bucket

   # хорошо
   def add(item, bucket: list | None = None):
       bucket = [] if bucket is None else bucket
       bucket.append(item)
       return bucket
   ```

2. **Сравнение с `None` через `==`** — используйте `is None`.
3. **Изменение списка во время итерации** — итерируйтесь по копии или создавайте новый список.
4. **Голый `except:`** — ловите конкретные исключения.
5. **Конкатенация строк в цикле** — используйте `"".join(parts)`.
6. **Отсутствие виртуального окружения** — используйте `uv` или `venv`.
7. **Открытие файлов без `with`** и без `encoding="utf-8"`.
8. **`from module import *`** — засоряет пространство имён.

---

## Вопросы с собеседований по Python

- Чем список отличается от кортежа? Что такое изменяемые и неизменяемые типы?
- Как работает GIL и что изменилось в free-threaded Python 3.13/3.14?
- В чём разница между `is` и `==`?
- Что такое генератор и чем `yield` отличается от `return`?
- Как устроен словарь (`dict`) и почему ключ должен быть хешируемым?
- Что такое декоратор? Напишите декоратор с параметрами.
- Чем `asyncio` отличается от `threading` и `multiprocessing`?
- Что такое MRO и как работает `super()`?
- Зачем нужны `__slots__`?
- Как работают контекстные менеджеры (`__enter__` / `__exit__`)?
- Поверхностное и глубокое копирование: `copy` vs `deepcopy`.
- Что такое `*args` и `**kwargs`?

**Продвинутый уровень (middle+ / senior):**

- Что такое дескриптор? Чем data descriptor отличается от non-data? Как устроен `property`?
- Когда нужен метакласс, а когда достаточно `__init_subclass__` или декоратора класса?
- Как работает `asyncio.TaskGroup` и что происходит с остальными задачами, если одна упала?
- Как ограничить число одновременных запросов в asyncio? Зачем джиттер в retry?
- Чем `contextvars` отличается от `threading.local` и почему это важно для asyncio?
- Что даёт free-threaded Python и какие проблемы он создаёт для существующего кода?
- Чем `ProcessPoolExecutor` отличается от `InterpreterPoolExecutor` (3.14)?
- Как найти утечку памяти? Что покажут `tracemalloc` и `gc.get_referrers`?
- Чем t-строки (PEP 750) отличаются от f-строк и зачем они нужны?
- Что такое `ParamSpec` и зачем он декораторам?
- Как реализовать Circuit Breaker и чем он отличается от retry?

---

## FAQ — частые вопросы

**С чего начать изучение Python в 2026 году?**
Установите Python 3.13 или 3.14 и `uv`, изучите базовый синтаксис, типы данных, функции, затем ООП и работу с файлами. После этого решайте задачи из раздела «Практика» и делайте мини-проекты.

**Какую версию Python выбрать?**
Для новых проектов — актуальную стабильную (3.13 или 3.14). Для рабочих проектов — ту, что поддерживают ваши зависимости.

**Нужна ли типизация в Python?**
Не обязательна, но в 2026 году это стандарт в командной разработке: меньше ошибок, лучше автодополнение, проще рефакторинг.

**Что лучше: pip или uv?**
`uv` значительно быстрее и объединяет управление версиями Python, окружениями и зависимостями. `pip` остаётся стандартным и работает везде.

**Где практиковаться в Python?**
Задачи из этого репозитория, LeetCode, Codewars, Stepik, Advent of Code, а также собственные pet-проекты.

**С чего начать продвинутые темы?**
С раздела [«Продвинутые темы»](#продвинутые-темы-python-middle--senior): запустите файлы из папки `advanced/`, прочитайте тесты и попробуйте изменить код так, чтобы тест упал, — это лучший способ понять, как всё работает.

**Как подготовиться к собеседованию Python-разработчика?**
Повторите базовые структуры данных, генераторы, декораторы, асинхронность, ООП, тестирование, SQL и Git. Решите 30–50 алгоритмических задач и подготовьте 1–2 проекта для портфолио.

---

## Полезные ресурсы

- [Официальная документация Python](https://docs.python.org/3/)
- [Что нового в Python 3.14](https://docs.python.org/3/whatsnew/3.14.html)
- [PEP 8 — руководство по стилю кода](https://peps.python.org/pep-0008/)
- [Real Python](https://realpython.com/)
- [Документация uv](https://docs.astral.sh/uv/)
- [Документация Ruff](https://docs.astral.sh/ruff/)
- [Документация FastAPI](https://fastapi.tiangolo.com/ru/)
- [Документация pytest](https://docs.pytest.org/)
- [Descriptor HowTo Guide](https://docs.python.org/3/howto/descriptor.html)
- [PEP 695 — синтаксис параметров типов](https://peps.python.org/pep-0695/)
- [PEP 750 — t-строки](https://peps.python.org/pep-0750/)
- [PEP 703 — Python без GIL](https://peps.python.org/pep-0703/)
- [Руководство по free-threaded Python](https://docs.python.org/3/howto/free-threading-python.html)

---

## Как помочь проекту

- Поставьте звезду репозиторию, чтобы его увидело больше разработчиков.
- Предложите свой пример кода или задачу через Pull Request.
- Нашли ошибку — создайте Issue.

---

**Теги:** `python` `python3` `python-примеры` `примеры-кода` `python-2026` `лучшие-практики` `чистый-код` `задачи-по-python` `python-для-начинающих` `asyncio` `fastapi` `pytest` `типизация` `собеседование-python` `python-3-14` `дескрипторы` `метаклассы` `free-threading` `contextvars` `паттерны-проектирования`

Лицензия: MIT
