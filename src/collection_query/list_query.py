from __future__ import annotations

from collection_query.field_lookups import FieldLookups


class ListQuery(list):
    def filter(self, **kwargs) -> ListQuery:
        return self._delete_condition_matching_items(**kwargs)

    def exclude(self, **kwargs) -> ListQuery:
        return self._delete_condition_matching_items(True, **kwargs)

    def _delete_condition_matching_items(self, exclude=False, **kwargs) -> ListQuery:
        if not kwargs:  # no conditions: nothing to match, leave collection untouched
            return self
        for i in range(len(self) - 1, -1, -1):  # going in reverse cause we deleting items
            matches = all(self._evaluate_condition(self[i], k, v) for k, v in kwargs.items())
            should_delete = matches if exclude else not matches
            if should_delete:
                del self[i]
        return self

    def _evaluate_condition(self, item, condition, value) -> bool:
        segments = condition.split("__")

        # The final segment may be a field lookup (e.g. ``__in``, ``__gt``); the
        # preceding segments are always nested keys to traverse.
        lookup = None
        if len(segments) > 1 and callable(func := getattr(FieldLookups, f"_{segments[-1]}", None)):
            lookup = func
            segments = segments[:-1]

        for key in segments:
            if isinstance(item, dict) and key in item:
                item = item[key]
            else:
                return False  # missing field/branch never matches

        return lookup(item, value) if lookup else item == value
