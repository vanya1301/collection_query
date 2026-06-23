from __future__ import annotations

import unittest

from collection_query import FieldLookupError, ListQuery


class StrictLookupTestCase(unittest.TestCase):
    """Unknown lookups must raise instead of silently returning no matches."""

    def setUp(self):
        self.data = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ]

    def test_unknown_lookup_on_scalar_raises(self):
        with self.assertRaises(FieldLookupError):
            ListQuery(self.data).filter(id__bogus=1)

    def test_unknown_lookup_message_lists_available(self):
        with self.assertRaises(FieldLookupError) as ctx:
            ListQuery(self.data).filter(id__notalookup=1)
        self.assertIn("notalookup", str(ctx.exception))
        self.assertIn("contains", str(ctx.exception))  # a real lookup is listed

    def test_absent_top_level_field_does_not_raise(self):
        # An absent field is a legit non-match, not an error.
        lq = ListQuery(self.data).filter(missing_field="x")
        self.assertEqual(list(lq), [])

    def test_nested_absent_key_does_not_raise(self):
        nested = [{"id": 1, "car": {"name": "Toyota"}}]  # no "country"
        lq = ListQuery(nested).filter(car__country="Japan")
        self.assertEqual(list(lq), [])

    def test_descend_into_non_dict_midpath_raises(self):
        nested = [{"id": 1, "car": "Toyota"}]  # car is a scalar, not a dict
        with self.assertRaises(FieldLookupError):
            ListQuery(nested).filter(car__country="Japan")

    def test_in_range_bad_value_raises(self):
        with self.assertRaises(FieldLookupError):
            ListQuery(self.data).filter(id__in_range=(1, 2, 3))


if __name__ == '__main__':
    unittest.main()
