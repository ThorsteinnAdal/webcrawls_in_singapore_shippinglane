__author__ = 'thorsteinn'

import unittest
from db_format_helpers.set_blanks_to_None import set_blanks_to_None
from db_format_helpers.list_all_field_values import list_all_field_values


class MyTestCase(unittest.TestCase):

    def set_up_db(self):
        db = {'ship1': {'key1': u'', 'key2': u'', 'key3': [['ape', 'cloth', 'rand'], [1, 2, 3]], 'key4': ' sometext ', 'key5': 1, 'key6': u'12'},
              'ship2': {'key1': 12, 'key2': u'', 'key3': [['ape', 'cloth', 'rand'], [2, 2, 2]], 'key4': '  sometext  ', 'key5': 11, 'key6': u'11'},
              'ship3': {'key1': u'ab', 'key2': u' \n  ', 'key3': [['ape', 'cloth', 'rand'], [3, 2, 3]], 'key4': '  sometext ', 'key5': 0, 'key6': u'0'},
              'ship4': {'key1': u'  ', 'key2': u'', 'key3': [['ape', 'cloth', 'rand'], [1, 2, 3]], 'key4': ' sometext\n', 'key5': 11.1, 'key6': u'11.1'}}
        return db

    def test_set_blanks_to_None_default(self):
        db = self.set_up_db()
        original_key1 = list_all_field_values('key1', db)
        original_key2 = list_all_field_values('key2', db)
        original_key3 = list_all_field_values('key3', db)
        original_key4 = list_all_field_values('key4', db)
        original_key5 = list_all_field_values('key5', db)
        original_key6 =list_all_field_values('key6', db)

        self.assertListEqual(sorted([u'', 12, u'ab', u'  ']), sorted(original_key1))
        set_blanks_to_None('key1', db)
        changed_key1 = list_all_field_values('key1', db)
        self.assertListEqual(sorted([None, 12, u'ab', None]), sorted(changed_key1))
        self.assertListEqual(sorted([u'', u'', u' \n  ', u'']), sorted(original_key2))
        self.assertListEqual(sorted([[['ape', 'cloth', 'rand'], [1, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [2, 2, 2]],
                                     [['ape', 'cloth', 'rand'], [3, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [1, 2, 3]]]), sorted(original_key3))
        self.assertListEqual(sorted([' sometext ', '  sometext  ', '  sometext ', ' sometext\n']), sorted(original_key4))
        self.assertListEqual(sorted([1, 11, 0, 11.1]), sorted(original_key5))
        self.assertListEqual(sorted([u'12', u'11', u'0', u'11.1']), sorted(original_key6))

        set_blanks_to_None('key2', db)
        changed_key2 = list_all_field_values('key2', db)
        self.assertListEqual(sorted([None, 12, u'ab', None]), sorted(changed_key1))
        self.assertListEqual(sorted([None, None, None, None]), sorted(changed_key2))
        self.assertListEqual(sorted([[['ape', 'cloth', 'rand'], [1, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [2, 2, 2]],
                                     [['ape', 'cloth', 'rand'], [3, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [1, 2, 3]]]), sorted(original_key3))
        self.assertListEqual(sorted([' sometext ', '  sometext  ', '  sometext ', ' sometext\n']), sorted(original_key4))
        self.assertListEqual(sorted([1, 11, 0, 11.1]), sorted(original_key5))
        self.assertListEqual(sorted([u'12', u'11', u'0', u'11.1']), sorted(original_key6))

        set_blanks_to_None('key3', db)
        changed_key3 = list_all_field_values('key3', db)
        self.assertListEqual(sorted([None, 12, u'ab', None]), sorted(changed_key1))
        self.assertListEqual(sorted([None, None, None, None]), sorted(changed_key2))
        self.assertListEqual(sorted([[['ape', 'cloth', 'rand'], [1, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [2, 2, 2]],
                                     [['ape', 'cloth', 'rand'], [3, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [1, 2, 3]]]), sorted(changed_key3))
        self.assertListEqual(sorted([' sometext ', '  sometext  ', '  sometext ', ' sometext\n']), sorted(original_key4))
        self.assertListEqual(sorted([1, 11, 0, 11.1]), sorted(original_key5))
        self.assertListEqual(sorted([u'12', u'11', u'0', u'11.1']), sorted(original_key6))

        set_blanks_to_None('key4', db)
        changed_key4 = list_all_field_values('key4', db)
        self.assertListEqual(sorted([None, 12, u'ab', None]), sorted(changed_key1))
        self.assertListEqual(sorted([None, None, None, None]), sorted(changed_key2))
        self.assertListEqual(sorted([[['ape', 'cloth', 'rand'], [1, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [2, 2, 2]],
                                     [['ape', 'cloth', 'rand'], [3, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [1, 2, 3]]]), sorted(changed_key3))
        self.assertListEqual(sorted([' sometext ', '  sometext  ', '  sometext ', ' sometext\n']), sorted(changed_key4))
        self.assertListEqual(sorted([1, 11, 0, 11.1]), sorted(original_key5))
        self.assertListEqual(sorted([u'12', u'11', u'0', u'11.1']), sorted(original_key6))

        set_blanks_to_None('key5', db)
        changed_key5 = list_all_field_values('key5', db)
        self.assertListEqual(sorted([None, 12, u'ab', None]), sorted(changed_key1))
        self.assertListEqual(sorted([None, None, None, None]), sorted(changed_key2))
        self.assertListEqual(sorted([[['ape', 'cloth', 'rand'], [1, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [2, 2, 2]],
                                     [['ape', 'cloth', 'rand'], [3, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [1, 2, 3]]]), sorted(changed_key3))
        self.assertListEqual(sorted([' sometext ', '  sometext  ', '  sometext ', ' sometext\n']), sorted(changed_key4))
        self.assertListEqual(sorted([1, 11, 0, 11.1]), sorted(changed_key5))
        self.assertListEqual(sorted([u'12', u'11', u'0', u'11.1']), sorted(original_key6))


        set_blanks_to_None('key6', db)
        changed_key6 =list_all_field_values('key6', db)
        self.assertListEqual(sorted([None, 12, u'ab', None]), sorted(changed_key1))
        self.assertListEqual(sorted([None, None, None, None]), sorted(changed_key2))
        self.assertListEqual(sorted([[['ape', 'cloth', 'rand'], [1, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [2, 2, 2]],
                                     [['ape', 'cloth', 'rand'], [3, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [1, 2, 3]]]), sorted(changed_key3))
        self.assertListEqual(sorted([' sometext ', '  sometext  ', '  sometext ', ' sometext\n']), sorted(changed_key4))
        self.assertListEqual(sorted([1, 11, 0, 11.1]), sorted(changed_key5))
        self.assertListEqual(sorted([u'12', u'11', u'0', u'11.1']), sorted(changed_key6))


    def test_set_blanks_to_None_mayhem(self):
        db = self.set_up_db()
        original_key1 = list_all_field_values('key1', db)
        original_key2 = list_all_field_values('key2', db)
        original_key3 = list_all_field_values('key3', db)
        original_key4 = list_all_field_values('key4', db)
        original_key5 = list_all_field_values('key5', db)
        original_key6 =list_all_field_values('key6', db)

        self.assertListEqual(sorted([u'', 12, u'ab', u'  ']), sorted(original_key1))
        set_blanks_to_None('key1', db, trailing_blanks=True)
        changed_key1 = list_all_field_values('key1', db)
        self.assertListEqual(sorted([None, 12, u'ab', None]), sorted(changed_key1))
        self.assertListEqual(sorted([u'', u'', u' \n  ', u'']), sorted(original_key2))
        self.assertListEqual(sorted([[['ape', 'cloth', 'rand'], [1, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [2, 2, 2]],
                                     [['ape', 'cloth', 'rand'], [3, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [1, 2, 3]]]), sorted(original_key3))
        self.assertListEqual(sorted([' sometext ', '  sometext  ', '  sometext ', ' sometext\n']), sorted(original_key4))
        self.assertListEqual(sorted([1, 11, 0, 11.1]), sorted(original_key5))
        self.assertListEqual(sorted([u'12', u'11', u'0', u'11.1']), sorted(original_key6))

        set_blanks_to_None('key2', db, trailing_blanks=True)
        changed_key2 = list_all_field_values('key2', db)
        self.assertListEqual(sorted([None, 12, u'ab', None]), sorted(changed_key1))
        self.assertListEqual(sorted([None, None, None, None]), sorted(changed_key2))
        self.assertListEqual(sorted([[['ape', 'cloth', 'rand'], [1, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [2, 2, 2]],
                                     [['ape', 'cloth', 'rand'], [3, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [1, 2, 3]]]), sorted(original_key3))
        self.assertListEqual(sorted([' sometext ', '  sometext  ', '  sometext ', ' sometext\n']), sorted(original_key4))
        self.assertListEqual(sorted([1, 11, 0, 11.1]), sorted(original_key5))
        self.assertListEqual(sorted([u'12', u'11', u'0', u'11.1']), sorted(original_key6))

        set_blanks_to_None('key3', db, trailing_blanks=True)
        changed_key3 = list_all_field_values('key3', db)
        self.assertListEqual(sorted([None, 12, u'ab', None]), sorted(changed_key1))
        self.assertListEqual(sorted([None, None, None, None]), sorted(changed_key2))
        self.assertListEqual(sorted([[['ape', 'cloth', 'rand'], [1, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [2, 2, 2]],
                                     [['ape', 'cloth', 'rand'], [3, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [1, 2, 3]]]), sorted(changed_key3))
        self.assertListEqual(sorted([' sometext ', '  sometext  ', '  sometext ', ' sometext\n']), sorted(original_key4))
        self.assertListEqual(sorted([1, 11, 0, 11.1]), sorted(original_key5))
        self.assertListEqual(sorted([u'12', u'11', u'0', u'11.1']), sorted(original_key6))

        set_blanks_to_None('key4', db, trailing_blanks=True)
        changed_key4 = list_all_field_values('key4', db)
        self.assertListEqual(sorted([None, 12, u'ab', None]), sorted(changed_key1))
        self.assertListEqual(sorted([None, None, None, None]), sorted(changed_key2))
        self.assertListEqual(sorted([[['ape', 'cloth', 'rand'], [1, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [2, 2, 2]],
                                     [['ape', 'cloth', 'rand'], [3, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [1, 2, 3]]]), sorted(changed_key3))
        self.assertListEqual(sorted(['sometext', 'sometext', 'sometext', 'sometext']), sorted(changed_key4))
        self.assertListEqual(sorted([1, 11, 0, 11.1]), sorted(original_key5))
        self.assertListEqual(sorted([u'12', u'11', u'0', u'11.1']), sorted(original_key6))

        set_blanks_to_None('key5', db, trailing_blanks=True)
        changed_key5 = list_all_field_values('key5', db)
        self.assertListEqual(sorted([None, 12, u'ab', None]), sorted(changed_key1))
        self.assertListEqual(sorted([None, None, None, None]), sorted(changed_key2))
        self.assertListEqual(sorted([[['ape', 'cloth', 'rand'], [1, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [2, 2, 2]],
                                     [['ape', 'cloth', 'rand'], [3, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [1, 2, 3]]]), sorted(changed_key3))
        self.assertListEqual(sorted(['sometext', 'sometext', 'sometext', 'sometext']), sorted(changed_key4))
        self.assertListEqual(sorted([1, 11, 0, 11.1]), sorted(changed_key5))
        self.assertListEqual(sorted([u'12', u'11', u'0', u'11.1']), sorted(original_key6))


        set_blanks_to_None('key6', db, trailing_blanks=True)
        changed_key6 =list_all_field_values('key6', db)
        self.assertListEqual(sorted([None, 12, u'ab', None]), sorted(changed_key1))
        self.assertListEqual(sorted([None, None, None, None]), sorted(changed_key2))
        self.assertListEqual(sorted([[['ape', 'cloth', 'rand'], [1, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [2, 2, 2]],
                                     [['ape', 'cloth', 'rand'], [3, 2, 3]],
                                     [['ape', 'cloth', 'rand'], [1, 2, 3]]]), sorted(changed_key3))
        self.assertListEqual(sorted(['sometext', 'sometext', 'sometext', 'sometext']), sorted(changed_key4))
        self.assertListEqual(sorted([1, 11, 0, 11.1]), sorted(changed_key5))
        self.assertListEqual(sorted([u'12', u'11', u'0', u'11.1']), sorted(changed_key6))

if __name__ == '__main__':
    unittest.main()
