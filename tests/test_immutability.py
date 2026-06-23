from __future__ import annotations

import unittest

from collection_query import ListQuery


class ImmutabilityTestCase(unittest.TestCase):
    """filter/exclude must not mutate the source or the object passed in."""

    def setUp(self):
        self.source = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Charlie"},
        ]

    def test_filter_does_not_mutate_input_list(self):
        original = list(self.source)
        ListQuery(self.source).filter(id=1)
        self.assertEqual(self.source, original)
        self.assertEqual(len(self.source), 3)

    def test_filter_does_not_mutate_listquery_instance(self):
        lq = ListQuery(self.source)
        result = lq.filter(id=1)
        self.assertEqual(len(lq), 3)  # original unchanged
        self.assertEqual([i["id"] for i in result], [1])

    def test_exclude_does_not_mutate_instance(self):
        lq = ListQuery(self.source)
        result = lq.exclude(id=1)
        self.assertEqual(len(lq), 3)
        self.assertEqual([i["id"] for i in result], [2, 3])

    def test_filter_returns_new_listquery(self):
        lq = ListQuery(self.source)
        result = lq.filter(id=1)
        self.assertIsInstance(result, ListQuery)
        self.assertIsNot(result, lq)

    def test_chaining_is_independent(self):
        lq = ListQuery(self.source)
        first = lq.filter(id__gte=2)
        second = first.exclude(name="Bob")
        self.assertEqual([i["id"] for i in lq], [1, 2, 3])
        self.assertEqual([i["id"] for i in first], [2, 3])
        self.assertEqual([i["id"] for i in second], [3])

    def test_empty_filter_returns_independent_copy(self):
        lq = ListQuery(self.source)
        result = lq.filter()
        self.assertIsNot(result, lq)
        self.assertEqual(result, lq)


if __name__ == '__main__':
    unittest.main()
