from __future__ import annotations

import unittest

from collection_query import FieldLookups, ListQuery


class IntrospectionTestCase(unittest.TestCase):

    def test_available_lookups_includes_builtins(self):
        names = ListQuery.available_lookups()
        for expected in ("in", "not", "in_range", "lt", "contains", "isnull", "exists"):
            self.assertIn(expected, names)

    def test_available_lookups_is_sorted(self):
        names = ListQuery.available_lookups()
        self.assertEqual(names, sorted(names))

    def test_fieldlookups_names_matches_listquery(self):
        self.assertEqual(FieldLookups.names(), ListQuery.available_lookups())


class RegistrationTestCase(unittest.TestCase):

    def tearDown(self):
        # Remove any custom lookups registered during tests.
        for name in ("iseven", "isodd"):
            if hasattr(FieldLookups, f"_{name}"):
                delattr(FieldLookups, f"_{name}")

    def test_register_direct(self):
        FieldLookups.register("iseven", lambda item, value: (item % 2 == 0) == value)
        self.assertIn("iseven", FieldLookups.names())
        data = [{"n": 1}, {"n": 2}, {"n": 3}, {"n": 4}]
        lq = ListQuery(data).filter(n__iseven=True)
        self.assertEqual([i["n"] for i in lq], [2, 4])

    def test_register_decorator(self):
        @FieldLookups.register("isodd")
        def is_odd(item, value):
            return (item % 2 == 1) == value

        data = [{"n": 1}, {"n": 2}, {"n": 3}]
        lq = ListQuery(data).filter(n__isodd=True)
        self.assertEqual([i["n"] for i in lq], [1, 3])


if __name__ == '__main__':
    unittest.main()
