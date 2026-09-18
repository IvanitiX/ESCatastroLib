from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def to_str(value: Any, *, strip: bool = True) -> str | None:
    """
    Convierte un valor a str.

    Devuelve None para valores nulos o cadenas vacías.
    """
    if value is None:
        return None

    result = str(value)

    if strip:
        result = result.strip()

    return result or None


def to_int(value: Any) -> int | None:
    """
    Convierte un valor a int.

    Devuelve None si el valor está vacío o no es convertible.
    """
    if value is None or value == "":
        return None

    if isinstance(value, bool):
        return int(value)

    try:
        return int(value)
    except (TypeError, ValueError):
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return None


def to_float(value: Any) -> float | None:
    """
    Convierte un valor a float.

    Acepta también cadenas con coma decimal.
    """
    if value is None or value == "":
        return None

    if isinstance(value, str):
        value = value.strip().replace(",", ".")

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def to_bool(value: Any, *, default: bool = False) -> bool:
    """
    Convierte valores habituales a booleanos.
    """
    if value is None or value == "":
        return default

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        normalized = value.strip().lower()

        if normalized in {"true", "1", "yes", "y", "si", "sí", "s"}:
            return True

        if normalized in {"false", "0", "no", "n"}:
            return False

    if isinstance(value, (int, float)):
        return value != 0

    return default


def to_dict(value: Any) -> dict[str, Any] | None:
    """
    Devuelve el valor si es un mapping; en otro caso, None.
    """
    if isinstance(value, Mapping):
        return dict(value)

    return None