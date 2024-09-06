from __future__ import annotations


class ListQuery(list):

    def filter(self, **kwargs) -> ListQuery:
        return self._delete_condition_matching_items(**kwargs)

    def exclude(self, **kwargs) -> ListQuery:
        return self._delete_condition_matching_items(True, **kwargs)

    def _delete_condition_matching_items(self, exclude=False, **kwargs) -> ListQuery:
        for i in range(len(self) - 1, -1, -1):
            if hasattr(self[i], "get") and callable(self[i].get):
                condition_result = all([self[i].get(k) == v for k, v in kwargs.items()])
                condition_result = condition_result if exclude else not condition_result
                if condition_result:
                    del self[i]
        return self
