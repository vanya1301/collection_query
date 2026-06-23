from __future__ import annotations

import unittest

from collection_query import ListQuery
from tests.test_data.data import data


class EdgeCasesTestCase(unittest.TestCase):

    def test_exclude_without_arguments_is_noop(self):
        # An argument-less exclude must not wipe the collection.
        lq = ListQuery(data).exclude()
        self.assertEqual(len(lq), len(data))
        self.assertEqual(lq, data)

    def test_filter_without_arguments_keeps_everything(self):
        lq = ListQuery(data).filter()
        self.assertEqual(len(lq), len(data))
        self.assertEqual(lq, data)

    def test_filter_equality_against_nested_subdict(self):
        # Equality against a whole sub-dict should compare the resolved branch,
        # not re-index by the first path segment.
        nested = [
            {"id": 1, "a": {"b": {"c": 1}}},
            {"id": 2, "a": {"b": {"c": 2}}},
        ]
        lq = ListQuery(nested).filter(a__b={"c": 1})
        self.assertEqual([i["id"] for i in lq], [1])

    def test_filter_drops_non_dict_items(self):
        # filter keeps only matches; non-dict items can never match.
        mixed = [{"id": 1}, "not-a-dict", {"id": 2}]
        lq = ListQuery(mixed).filter(id=1)
        self.assertEqual(lq, [{"id": 1}])

    def test_exclude_keeps_non_dict_items(self):
        mixed = [{"id": 1}, "not-a-dict", {"id": 2}]
        lq = ListQuery(mixed).exclude(id=1)
        self.assertEqual(lq, ["not-a-dict", {"id": 2}])


if __name__ == '__main__':
    unittest.main()
