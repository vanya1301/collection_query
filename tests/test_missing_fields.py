from __future__ import annotations

import unittest

from collection_query import ListQuery
from tests.test_data.data import sparse_data, sparse_nested_data


class MissingFieldsTestCase(unittest.TestCase):
    """Covers querying heterogeneous data where fields may be absent."""

    def test_filter_missing_top_level_field_no_keyerror(self):
        # Items lacking the queried field should be treated as non-matching,
        # not raise KeyError.
        lq = ListQuery(sparse_data).filter(first_name="Blane")
        self.assertEqual([i["id"] for i in lq], [1])

    def test_filter_missing_top_level_field_with_lookup(self):
        lq = ListQuery(sparse_data).filter(car_make__startswith="Ch")
        self.assertEqual([i["id"] for i in lq], [1])

    def test_exclude_missing_top_level_field(self):
        # Exclude must keep items that lack the field (they don't match).
        lq = ListQuery(sparse_data).exclude(first_name="Blane")
        self.assertEqual([i["id"] for i in lq], [2, 3, 4])

    def test_filter_missing_nested_branch_no_error(self):
        lq = ListQuery(sparse_nested_data).filter(car__country="Japan")
        self.assertEqual([i["id"] for i in lq], [4])

    def test_filter_missing_nested_branch_with_lookup(self):
        # Item 3 has no "car"; item 2 has no "country" -> neither should error.
        lq = ListQuery(sparse_nested_data).filter(car__country__startswith="J")
        self.assertEqual([i["id"] for i in lq], [4])

    def test_filter_missing_nested_branch_with_comparison_lookup(self):
        lq = ListQuery(sparse_nested_data).filter(car__country__in=["Italy", "Japan"])
        self.assertEqual([i["id"] for i in lq], [1, 4])

    def test_exclude_missing_nested_branch(self):
        lq = ListQuery(sparse_nested_data).exclude(car__country="Japan")
        self.assertEqual([i["id"] for i in lq], [1, 2, 3])


if __name__ == '__main__':
    unittest.main()
