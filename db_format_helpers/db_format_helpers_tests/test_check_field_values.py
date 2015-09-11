__author__ = 'thorsteinn'

import unittest
from db_format_helpers.check_field_values import check_field_values


class MyTestCase(unittest.TestCase):

    def set_up_db(self):
        db = {'ship1': {'key1': u'', 'key2': u'', 'key3': [['ape', 'cloth', 'rand'], [1, 2, 3]], 'key4': 'sometext', 'key5': 1, 'key6': u'12'},
              'ship2': {'key1': 12, 'key2': u'', 'key3': [['ape', 'cloth', 'rand'], [2, 2, 2]], 'key4': 'sometext', 'key5': 11, 'key6': u'11'},
              'ship3': {'key1': u'ab', 'key2': u' \n  ', 'key3': [['ape', 'cloth', 'rand'], [3, 2, 3]], 'key4': 'sometext', 'key5': 0, 'key6': u'0'},
              'ship4': {'key1': u'  ', 'key2': u'', 'key3': [['ape', 'cloth', 'rand'], [1, 2, 3]], 'key4': 'sometext', 'key5': 11.1, 'key6': u'11.1'}}
        return db

    def test_check_field_values(self):
        db = self.set_up_db()
        self.assertTrue(check_field_values('key1', db, has_blanks=True),
                        msg="key1 has blanks, some text and some numbers")
        self.assertTrue(check_field_values('key2', db, has_blanks=True),
                        msg="key2 has all blanks")
        self.assertFalse(check_field_values('key3', db, has_blanks=True),
                         msg="key3 has no blanks and lists only")
        self.assertFalse(check_field_values('key4', db, has_blanks=True),
                         msg="key4 has all regular strings")
        self.assertFalse(check_field_values('key5', db, has_blanks=True),
                         msg="key5 has all numbers")
        self.assertFalse(check_field_values('key6', db, has_blanks=True),
                         msg="key6 has all numbers as string")

        self.assertFalse(check_field_values('key1', db, has_all_blanks=True),
                         msg="key1 has blanks, some text and some numbers")
        self.assertTrue(check_field_values('key2', db, has_all_blanks=True),
                        msg="key2 has all blanks")
        self.assertFalse(check_field_values('key3', db, has_all_blanks=True),
                         msg="key3 has no blanks and lists only")
        self.assertFalse(check_field_values('key4', db, has_all_blanks=True),
                         msg="key4 has all regular strings")
        self.assertFalse(check_field_values('key5', db, has_all_blanks=True),
                         msg="key5 has all numbers")
        self.assertFalse(check_field_values('key6', db, has_all_blanks=True),
                         msg="key6 has all numbers as string")

        self.assertFalse(check_field_values('key1', db, has_no_blanks=True),
                         msg="key1 has blanks, some text and some numbers")
        self.assertFalse(check_field_values('key2', db, has_no_blanks=True),
                         msg="key2 has all blanks")
        self.assertTrue(check_field_values('key3', db, has_no_blanks=True),
                        msg="key3 has no blanks and lists only")
        self.assertTrue(check_field_values('key4', db, has_no_blanks=True),
                        msg="key4 has all regular strings")
        self.assertTrue(check_field_values('key5', db, has_no_blanks=True),
                        msg="key5 has all numbers")
        self.assertTrue(check_field_values('key6', db, has_no_blanks=True),
                        msg="key6 has all numbers as string")

        self.assertFalse(check_field_values('key1', db, has_all_numbers=True),
                         msg="key1 has blanks, some text and some numbers")
        self.assertFalse(check_field_values('key2', db, has_all_numbers=True),
                         msg="key2 has all blanks")
        self.assertFalse(check_field_values('key3', db, has_all_numbers=True),
                         msg="key3 has no blanks and lists only")
        self.assertFalse(check_field_values('key4', db, has_all_numbers=True),
                         msg="key4 has all regular strings")
        self.assertTrue(check_field_values('key5', db, has_all_numbers=True),
                        msg="key5 has all numbers")
        self.assertFalse(check_field_values('key6', db, has_all_numbers=True),
                         msg="key6 has all numbers as string")

        self.assertFalse(check_field_values('key1', db, has_all_text=True),
                         msg="key1 has blanks, some text and some numbers")
        self.assertTrue(check_field_values('key2', db, has_all_text=True),
                         msg="key2 has all blanks")
        self.assertFalse(check_field_values('key3', db, has_all_text=True),
                         msg="key3 has no blanks and lists only")
        self.assertTrue(check_field_values('key4', db, has_all_text=True),
                        msg="key4 has all regular strings")
        self.assertFalse(check_field_values('key5', db, has_all_text=True),
                         msg="key5 has all numbers")
        self.assertTrue(check_field_values('key6', db, has_all_text=True),
                        msg="key6 has all numbers as string")

if __name__ == '__main__':
    unittest.main()
