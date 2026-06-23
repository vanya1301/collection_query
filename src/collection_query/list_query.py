from __future__ import annotations

from typing import List, TypeVar

from collection_query.field_lookups import MISSING, FieldLookupError, FieldLookups

T = TypeVar("T")


class ListQuery(List[T]):
    """A ``list`` with Django-style ``filter``/``exclude`` querying.

    ``filter`` and ``exclude`` are non-mutating: they return a new ``ListQuery``
    and never modify the original collection (nor the object passed to the
    constructor). Chaining therefore produces independent results.
    """

    def filter(self, **kwargs) -> ListQuery[T]:
        """Return a new ListQuery keeping items that match ALL conditions."""
        return self._apply(kwargs, keep_matching=True)

    def exclude(self, **kwargs) -> ListQuery[T]:
        """Return a new ListQuery dropping items that match ALL conditions."""
        return self._apply(kwargs, keep_matching=False)

    @classmethod
    def available_lookups(cls) -> list:
        """Return the sorted names of all registered field lookups."""
        return FieldLookups.names()

    def _apply(self, conditions: dict, keep_matching: bool) -> ListQuery[T]:
        if not conditions:  # no conditions: return an independent copy unchanged
            return ListQuery(self)
        return ListQuery(
            item
            for item in self
            if self._matches_all(item, conditions) is keep_matching
        )

    def _matches_all(self, item, conditions: dict) -> bool:
        return all(
            self._evaluate_condition(item, key, value)
            for key, value in conditions.items()
        )

    def _evaluate_condition(self, item, condition: str, value) -> bool:
        *path, last = condition.split("__")
        lookup = FieldLookups.get(last)

        if lookup is None:
            # No trailing lookup: the whole condition is a field path, compared
            # for equality against ``value``.
            resolved = self._resolve(item, [*path, last])
            return resolved is not MISSING and resolved == value

        if last in FieldLookups.PRESENCE_LOOKUPS:
            # Presence lookups must see absence, so don't short-circuit on MISSING.
            return lookup(self._resolve(item, path), value)

        resolved = self._resolve(item, path)
        if resolved is MISSING:
            return False  # field absent -> non-match for value lookups
        return lookup(resolved, value)

    def _resolve(self, item, path: list):
        """Walk ``path`` of nested dict keys.

        Returns ``MISSING`` when a key is absent from a mapping (legit ragged
        data) or when the root item itself is not a mapping. Raises
        ``FieldLookupError`` if the path tries to descend into a non-mapping
        AFTER already traversing into the structure -- a strong signal that the
        trailing segment was an unknown/typo'd lookup (e.g. ``id__bogus``).
        """
        current = item
        descended = False
        for key in path:
            if isinstance(current, dict):
                if key in current:
                    current = current[key]
                    descended = True
                else:
                    return MISSING  # field absent in this record -> non-match
            elif not descended:
                return MISSING  # root item isn't a mapping -> non-match
            else:
                raise FieldLookupError(
                    f"Cannot apply {key!r} to non-mapping value {current!r}: "
                    f"{key!r} is not a registered lookup. "
                    f"Available lookups: {', '.join(FieldLookups.names())}."
                )
        return current
