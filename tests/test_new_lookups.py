from __future__ import annotations

import unittest

from collection_query import ListQuery


class NewLookupsTestCase(unittest.TestCase):
    """Covers lookups added in 0.2.0: case-insensitive, regex, presence, ranges."""

    def setUp(self):
        self.data = [
            {"id": 1, "name": "Alice", "email": "alice@Example.com"},
            {"id": 2, "name": "bob", "email": "BOB@example.org"},
            {"id": 3, "name": "Charlie", "email": None},
            {"id": 4, "name": "dave"},  # no email key
        ]

    def test_icontains(self):
        lq = ListQuery(self.data).filter(email__icontains="EXAMPLE")
        self.assertEqual([i["id"] for i in lq], [1, 2])

    def test_istartswith(self):
        lq = ListQuery(self.data).filter(name__istartswith="A")
        self.assertEqual([i["id"] for i in lq], [1])

    def test_iendswith(self):
        lq = ListQuery(self.data).filter(name__iendswith="E")
        self.assertEqual([i["id"] for i in lq], [1, 3, 4])

    def test_iexact(self):
        lq = ListQuery(self.data).filter(name__iexact="BOB")
        self.assertEqual([i["id"] for i in lq], [2])

    def test_regex(self):
        lq = ListQuery(self.data).filter(name__regex=r"^[A-Z]")
        self.assertEqual([i["id"] for i in lq], [1, 3])

    def test_iregex(self):
        lq = ListQuery(self.data).filter(name__iregex=r"^d")
        self.assertEqual([i["id"] for i in lq], [4])

    def test_in_range_tuple(self):
        lq = ListQuery(self.data).filter(id__in_range=(2, 4))
        self.assertEqual([i["id"] for i in lq], [2, 3])

    def test_in_range_list(self):
        lq = ListQuery(self.data).filter(id__in_range=[1, 2])
        self.assertEqual([i["id"] for i in lq], [1])

    def test_in_range_still_accepts_range(self):
        lq = ListQuery(self.data).filter(id__in_range=range(3, 5))
        self.assertEqual([i["id"] for i in lq], [3, 4])

    def test_exists_true(self):
        lq = ListQuery(self.data).filter(email__exists=True)
        self.assertEqual([i["id"] for i in lq], [1, 2, 3])

    def test_exists_false(self):
        lq = ListQuery(self.data).filter(email__exists=False)
        self.assertEqual([i["id"] for i in lq], [4])

    def test_isnull_true_matches_none_and_absent(self):
        # id 3 has email=None, id 4 has no email key at all.
        lq = ListQuery(self.data).filter(email__isnull=True)
        self.assertEqual([i["id"] for i in lq], [3, 4])

    def test_isnull_false(self):
        lq = ListQuery(self.data).filter(email__isnull=False)
        self.assertEqual([i["id"] for i in lq], [1, 2])


if __name__ == '__main__':
    unittest.main()
