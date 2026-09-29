"""Новые возможности Python 3.14 в коде.

* t-строки (PEP 750) — шаблоны, которые можно безопасно обработать
* отложенное вычисление аннотаций (PEP 649/749) и модуль annotationlib
* except без скобок (PEP 758)
* concurrent.interpreters — субинтерпретаторы в стандартной библиотеке (PEP 734)

Файл импортируется и на старых версиях, но демо запускается только на 3.14+.
Запуск: python3.14 -m advanced.python314
"""

from __future__ import annotations

import sys

PY314 = sys.version_info >= (3, 14)

# Синтаксис 3.14 нельзя положить в модуль, который должен парситься на 3.12,
# поэтому код с новым синтаксисом хранится строкой и компилируется по требованию.
_CODE_314 = r'''
from html import escape
from string.templatelib import Interpolation, Template


def html(template: Template) -> str:
    """Экранирует ТОЛЬКО подставленные значения, а не сам шаблон.
    С f-строкой так сделать невозможно: она сразу превращается в str."""
    parts: list[str] = []
    for item in template:
        if isinstance(item, Interpolation):
            parts.append(escape(str(item.value)))
        else:
            parts.append(item)
    return "".join(parts)


def sql(template: Template) -> tuple[str, list]:
    """Превращает t-строку в параметризованный запрос — защита от SQL-инъекций."""
    query: list[str] = []
    params: list = []
    for item in template:
        if isinstance(item, Interpolation):
            query.append("?")
            params.append(item.value)
        else:
            query.append(item)
    return "".join(query), params


def forward_ref_demo() -> dict:
    # аннотации вычисляются лениво: Node можно упомянуть до его определения
    # (без from __future__ import annotations и без кавычек)
    import annotationlib

    class Tree:
        root: Node

    class Node:
        value: int

    return annotationlib.get_annotations(Tree, format=annotationlib.Format.FORWARDREF)


def parse_int(value: str) -> int | None:
    try:
        return int(value)
    except ValueError, TypeError:  # PEP 758: скобки больше не обязательны
        return None


def demo() -> None:
    user_input = "<script>alert('xss')</script>"
    print(html(t"<p>Привет, {user_input}!</p>"))

    name = "Robert'); DROP TABLE students;--"
    print(sql(t"SELECT * FROM users WHERE name = {name} AND age > {18}"))

    print(forward_ref_demo())
    print(parse_int("42"), parse_int("abc"))
'''


def load() -> dict:
    """Скомпилировать и вернуть пространство имён с функциями 3.14."""
    if not PY314:
        raise RuntimeError("Нужен Python 3.14+")
    ns: dict = {"__name__": "advanced.python314_impl"}
    # dont_inherit=True — не наследовать `from __future__ import annotations` этого файла
    exec(compile(_CODE_314, __file__ + ":314", "exec", dont_inherit=True), ns)
    return ns


def main() -> None:
    if not PY314:
        print(f"Этот пример требует Python 3.14+, у вас {sys.version.split()[0]}")
        return
    load()["demo"]()


if __name__ == "__main__":
    main()
