import unittest
from list_query import ListQuery
from tests.test_data.data import *


class FieldsLookupTestCase(unittest.TestCase):
    def test_field_lookup_in(self):
        lq = ListQuery(data).filter(first_name__in=["Blane", "Samara"])
        self.assertTrue(len(lq))
        for i in lq:
            self.assertTrue(i["first_name"] in ["Blane", "Samara"])

    def test_field_lookup_not(self):
        lq = ListQuery(data).filter(car_make__not="Land Rover")
        self.assertTrue(len(lq))
        for i in lq:
            self.assertNotEqual(i['id'], "Land Rover")

    def test_field_lookup_in_range(self):
        lq = ListQuery(data).filter(id__in_range=range(1, 5))
        self.assertTrue(len(lq))
        for i in lq:
            self.assertTrue(0 < i['id'] < 5)

    def test_field_lookup_lt(self):
        lq = ListQuery(data).filter(id__lt=3)
        self.assertTrue(len(lq))
        for i in lq:
            self.assertTrue(i['id'] < 3)

    def test_field_lookup_lte(self):
        lq = ListQuery(data).filter(id__lte=3)
        self.assertTrue(len(lq))
        for i in lq:
            self.assertTrue(i['id'] <= 3)

    def test_field_lookup_gt(self):
        lq = ListQuery(data).filter(id__gt=3)
        self.assertTrue(len(lq))
        for i in lq:
            self.assertTrue(i['id'] > 3)

    def test_field_lookup_gte(self):
        lq = ListQuery(data).filter(id__gte=3)
        self.assertTrue(len(lq))
        for i in lq:
            self.assertTrue(i['id'] >= 3)

    def test_field_lookup_contains(self):
        lq = ListQuery(data).filter(ip_address__contains=".183.")

        self.assertTrue(len(lq))
        for i in lq:
            self.assertTrue(".183." in i['ip_address'])


if __name__ == '__main__':
    unittest.main()
