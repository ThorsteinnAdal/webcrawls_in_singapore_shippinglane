__author__ = 'thorsteinn'

import unittest
from db_format_helpers.strings_in_fields_to_numbers import strings_in_fields_to_numbers
from db_format_helpers.list_all_field_values import list_all_field_values
from db_format_helpers.is_number import is_number
from db_format_helpers.is_int import is_int


class MyTestCase(unittest.TestCase):
    def set_up_db(self):
        db = {
            'ship1':
                {u'name_s': 'SHIP 1',
                 u'machine_l': [[u'name', u'role', u'power', u'note'],
                                [u'Propulsion', u'Man B&W', u'14000'],
                                [u'Aux', u'Cat', u'400']],
                 u'length_f': u'42.115',
                 u'imo_id': u'12345678',
                 u'dnv_id': u'12233445',
                 u'all_have_this_id': u'123',
                 u'all_same_id': u'000011',
                 u'large_value': u'12,123,123'},
            'ship2':
                {u'name_s': 'SHIP 2',
                 u'machine_l': [[u'name', u'role', u'power', u'note'],
                                [u'Propulsion', u'Wartsilla', u'7800'],
                                [u'Aux', u'Volvo', u'30.115']],
                 u'length_f': u'41.115',
                 u'imo_id': u'',
                 u'dnv_id': u'12345678',
                 u'all_have_this_id': u'234',
                 u'all_same_id': u'000011',
                 u'large_value': u'123,123'},
            'ship3':
                {u'name_s': 'SHIP 3',
                 u'machine_l': [[u'name', u'role', u'power', u'note'],
                                [u'Propulsion', u'Volvo', u'800.15'],
                                [u'Aux', u'Cat', u'315']],
                 u'length_f': u'1,225.15',
                 u'imo_id': u'98765432',
                 u'dnv_id': u'',
                 u'all_have_this_id': u'456',
                 u'all_same_id': u'000011',
                 u'large_value': u'1,123'},
        }
        return db

    def test_string_in_fields_to_numbers(self):
        db = self.set_up_db()

        haul_pre = list_all_field_values('all_have_this_id', db)
        for val in haul_pre:
            self.assertTrue(is_int(val))
        strings_in_fields_to_numbers('all_have_this_id', db)
        haul_post = list_all_field_values('all_have_this_id', db)
        for val in haul_post:
            self.assertTrue(is_int(val))
        self.assertListEqual(sorted([123, 234, 456]), sorted(haul_post), msg="The two lists were not equal")

        strings_in_fields_to_numbers('all_same_id', db)
        haul_post = list_all_field_values('all_same_id', db)
        for val in haul_post:
            self.assertTrue(is_int(val))
        self.assertListEqual(sorted([11, 11, 11]), sorted(haul_post), msg="The two lists were not equal")

        haul = list_all_field_values('not_found', db)
        self.assertEqual(len(haul), 0, msg='Expected length to be 0, got length %s' % len(haul))
        strings_in_fields_to_numbers('not_found', db)

        haul_pre = list_all_field_values('length_f', db)
        for val in haul_pre:
            self.assertTrue(is_number(val), msg='The value %s is not a valid number' % str(val))
        strings_in_fields_to_numbers(None, db)
        haul_post = list_all_field_values('length_f', db)
        for val in haul_post:
            self.assertTrue(is_number(val), msg='The value %s is not a valid number' % str(val))
        self.assertListEqual(sorted([42.115, 41.115, 1225.15]), sorted(haul_post), msg="lists were not equal")

        haul = list_all_field_values('large_value', db)
        for val in haul:
            self.assertTrue(is_number(val), msg="{field} failed at value {value}".format(field='large_value', value=val))
        strings_in_fields_to_numbers('large_value', db)
        haul_post = list_all_field_values('large_value', db)
        for val in haul_post:
            self.assertTrue(is_number(val), msg="{field} failed at value {value}".format(field='large_value', value=val))
        self.assertListEqual(sorted([12123123, 123123, 1123]), sorted(haul_post), msg="lists were not equal")

if __name__ == '__main__':
    unittest.main()
