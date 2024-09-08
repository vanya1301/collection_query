import unittest
from list_query import ListQuery
from tests.test_data.data import *


class NestedFieldsTestCase(unittest.TestCase):

    def test_filter_nested_fields(self):
        lq = ListQuery(nested_dict_data).filter(car__country="Japan")

        len(lq)
        for i in lq:
            self.assertEqual(i["car"]["country"], "Japan")

    def test_exclude_nested_fields(self):
        lq = ListQuery(nested_dict_data).exclude(car__country="Unknown")

        len(lq)
        for i in lq:
            self.assertNotEqual(i["car"]["country"], "Unknown")

    def test_filter_nested_fields_with_field_lookups(self):
        lq = ListQuery(nested_dict_data).filter(car__country__in=["Japan", "Germany"])

        len(lq)
        for i in lq:
            self.assertIn(i["car"]["country"], ["Japan", "Germany"])

    def test_exclude_nested_fields_with_field_lookups(self):
        lq = ListQuery(nested_dict_data).exclude(car__country__in=["Japan", "Germany"])

        len(lq)
        for i in lq:
            self.assertNotIn(i["car"]["country"], ["Japan", "Germany"])


if __name__ == '__main__':
    unittest.main()
