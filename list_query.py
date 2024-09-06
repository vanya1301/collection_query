from __future__ import annotations

from field_lookups import FieldLookups


class ListQuery(list, FieldLookups):
    def filter(self, **kwargs) -> ListQuery:
        return self._pick_condition_matching_items(**kwargs)

    def exclude(self, **kwargs) -> ListQuery:
        return self._pick_condition_matching_items(True, **kwargs)

    def _pick_condition_matching_items(self, exclude=False, **kwargs) -> ListQuery:
        for i in self:
            if hasattr(i, "get") and callable(i.get):
                condition_result = all([self._evaluate_condition(i, k, v) for k, v in kwargs.items()])
                condition_result = not condition_result if exclude else condition_result
                if condition_result:
                    yield i

    def _evaluate_condition(self, item, condition, value) -> bool:
        field_lookups = condition.split("__")
        key = field_lookups.pop(0)
        for i in field_lookups:
            func = getattr(FieldLookups, f"_{i}")
            if func:
                return func(item.get(key), value)

        return item[key] == value
