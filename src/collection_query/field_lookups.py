from __future__ import annotations

import functools
import re
from typing import Callable


def _requires_str(func: Callable) -> Callable:
    """Wrap a string lookup so non-string values are non-matches, not errors.

    Nullable/heterogeneous fields (e.g. ``None`` or numbers) shouldn't crash a
    string lookup; they simply don't match.
    """

    @functools.wraps(func)
    def wrapper(item, value):
        if not isinstance(item, str):
            return False
        return func(item, value)

    return wrapper


class FieldLookupError(Exception):
    """Raised when a query uses a lookup name that is not registered.

    Distinguishes a programmer error (typo'd / unknown lookup) from the legit
    "field absent in this record" case, which is treated as a non-match.
    """


class _Missing:
    """Sentinel for "field not present" so presence lookups can detect absence."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "<MISSING>"

    def __bool__(self) -> bool:
        return False


# Single shared sentinel instance.
MISSING = _Missing()


class FieldLookups:
    """Registry of field-lookup operations.

    Each lookup is a ``staticmethod`` named ``_<lookup>`` so it is reachable as
    ``field__<lookup>=value`` in a query. Lookups receive the resolved field
    value and the comparison value and return a ``bool``.
    """

    # Lookups that must run even when the field is absent (receive ``MISSING``).
    PRESENCE_LOOKUPS = frozenset({"isnull", "exists"})

    # --- Membership -------------------------------------------------------
    @staticmethod
    def _in(item, value) -> bool:
        return item in value

    @staticmethod
    def _not(item, value) -> bool:
        return item != value

    @staticmethod
    def _in_range(item, value) -> bool:
        # Accept a real ``range`` or a 2-element ``(lo, hi)`` tuple/list.
        # Semantics match ``range``: half-open ``lo <= item < hi``.
        if isinstance(value, range):
            return item in value
        if isinstance(value, (tuple, list)) and len(value) == 2:
            lo, hi = value
            return lo <= item < hi
        raise FieldLookupError(
            "in_range expects a range or a 2-element (lo, hi) tuple/list, "
            f"got {value!r}."
        )

    # --- Comparisons ------------------------------------------------------
    @staticmethod
    def _lt(item, value) -> bool:
        return item < value

    @staticmethod
    def _lte(item, value) -> bool:
        return item <= value

    @staticmethod
    def _gt(item, value) -> bool:
        return item > value

    @staticmethod
    def _gte(item, value) -> bool:
        return item >= value

    # --- String matching (non-string values are treated as non-matches) ---
    @staticmethod
    @_requires_str
    def _startswith(item: str, value: str) -> bool:
        return item.startswith(value)

    @staticmethod
    @_requires_str
    def _endswith(item: str, value: str) -> bool:
        return item.endswith(value)

    @staticmethod
    @_requires_str
    def _contains(item: str, value: str) -> bool:
        return value in item

    @staticmethod
    @_requires_str
    def _icontains(item: str, value: str) -> bool:
        return value.lower() in item.lower()

    @staticmethod
    @_requires_str
    def _istartswith(item: str, value: str) -> bool:
        return item.lower().startswith(value.lower())

    @staticmethod
    @_requires_str
    def _iendswith(item: str, value: str) -> bool:
        return item.lower().endswith(value.lower())

    @staticmethod
    @_requires_str
    def _iexact(item: str, value: str) -> bool:
        return item.lower() == value.lower()

    @staticmethod
    @_requires_str
    def _regex(item: str, value: str) -> bool:
        return re.search(value, item) is not None

    @staticmethod
    @_requires_str
    def _iregex(item: str, value: str) -> bool:
        return re.search(value, item, re.IGNORECASE) is not None

    # --- Presence (receive MISSING when the field is absent) --------------
    @staticmethod
    def _isnull(item, value: bool) -> bool:
        is_null = item is MISSING or item is None
        return is_null == value

    @staticmethod
    def _exists(item, value: bool) -> bool:
        return (item is not MISSING) == value

    # --- Registry API -----------------------------------------------------
    @classmethod
    def get(cls, name: str) -> Callable | None:
        """Return the lookup callable for ``name``, or ``None`` if unregistered."""
        method = getattr(cls, f"_{name}", None)
        return method if callable(method) else None

    @classmethod
    def names(cls) -> list:
        """Return the sorted names of all registered lookups."""
        return sorted(
            attr[1:]
            for attr in dir(cls)
            if attr.startswith("_")
            and not attr.startswith("__")
            and callable(getattr(cls, attr))
        )

    @classmethod
    def register(cls, name: str, func: Callable | None = None):
        """Register a custom lookup. Usable directly or as a decorator.

        Direct:
            FieldLookups.register("iseven", lambda item, value: (item % 2 == 0) == value)

        Decorator:
            @FieldLookups.register("iseven")
            def is_even(item, value):
                return (item % 2 == 0) == value
        """

        def _apply(fn: Callable) -> Callable:
            setattr(cls, f"_{name}", staticmethod(fn))
            return fn

        return _apply(func) if func is not None else _apply
