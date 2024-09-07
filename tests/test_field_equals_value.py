import unittest
from list_query import ListQuery
from tests.test_data.data import data, data2


class EqualsConditionTestCase(unittest.TestCase):

    def setUp(self):
        self.test_first_name = "Donalt"

    def test_filter_equals_value(self):
        lq = ListQuery(data).filter(first_name=self.test_first_name)

        for i in lq:
            assert (i["first_name"] == self.test_first_name)

        donalts = [i for i in data if i["first_name"] == self.test_first_name]
        assert (lq == donalts)
        assert (len(lq))

    def test_exclude_equals_value(self):
        lq = ListQuery(data).exclude(first_name=self.test_first_name)

        for i in lq:
            assert (i["first_name"] != self.test_first_name)

        not_donalts = [i for i in data if i["first_name"] != self.test_first_name]
        assert (lq == not_donalts)
        assert (len(lq))

    def test_filter_equals_multiple_values(self):
        lq = ListQuery(data).filter(first_name=self.test_first_name, car_make="Toyota")

        for i in lq:
            assert (i["first_name"] == self.test_first_name)
            assert (i["car_make"] == "Toyota")

        donalts_toyota_drivers = [i for i in data if
                                  i["first_name"] == self.test_first_name and i["car_make"] == "Toyota"]
        assert (lq == donalts_toyota_drivers)
        assert (len(lq))

    def test_exclude_equals_multiple_values(self):
        lq = ListQuery(data).exclude(first_name=self.test_first_name, car_make="Toyota")

        for i in lq:
            assert (i["first_name"] != self.test_first_name or i["car_make"] != "Toyota")

        no_donalts_toyota_drivers = [i for i in data if
                                     i["first_name"] != self.test_first_name or i["car_make"] != "Toyota"]

        assert (lq == no_donalts_toyota_drivers)
        assert (len(lq))

    def test_nested_exclude_conditions(self):
        lq = ListQuery(data).exclude(first_name=self.test_first_name).exclude(car_make="Toyota")

        for i in lq:
            assert (i["first_name"] != self.test_first_name)
            assert (i["car_make"] != "Toyota")

        no_donalts_toyota_drivers = [i for i in data if
                                     i["first_name"] != self.test_first_name and i["car_make"] != "Toyota"]

        assert (lq == no_donalts_toyota_drivers)
        assert (len(lq))


if __name__ == '__main__':
    unittest.main()
