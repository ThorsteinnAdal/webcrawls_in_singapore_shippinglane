__author__ = 'thorsteinn'

import unittest
import os
import json
from jsonDicts_to_file import db_to_file, file_to_db, check_if_db_is_in_file, groom_file_db

class MyTestCase(unittest.TestCase):
    def setUp(self):
        '''
        make a reasonable looking dictionary
        '''
        first = {'header001': {'type': 'container vessel', 'callsign': 'br"olt', 'length': 14.114, 'width': 7.11}}
        second = {'header002': {'type': 'container vessel', 'callsign': 'mori', 'length': 10.114, 'width': 4.11}}
        secondmix = {'header002': {'callsign': 'mori', 'length': 10.114, 'width': 4.11, 'type': 'container vessel'}}
        third = {'header003': {'type': 'Ro-ro cargo', 'callsign': 'dora', 'length': 40.1, 'width': 7.11}}
        with open('test_jsonDict_to_file.txt', 'w') as f:
            json.dump(first,f)
            f.write('\n')
            json.dump(second,f)
            f.write('\n')
            json.dump(secondmix,f)
            f.write('\n')
            json.dump(second,f)
            f.write('\n')
            json.dump(third,f)
            f.write('\n')

    def test_db_to_file_to_db(self):
        db = {'a': {'aa': 'abcd', 'bb': 'bcde', 'cc': 'fghi'},
              'b': {'aa': 'efgh', 'bb': 'fghi', 'cc': 'fghi'},
              'c': {'aa': 'ijkl', 'bb': 'jklm', 'cc': 'fghi'},
              'd': {'aa': 'mnop', 'bb': 'nopq', 'cc': 'fghi'}}
        db_to_file(db, 'test_db_to_file_to_db.txt')
        samedb = file_to_db('test_db_to_file_to_db.txt')
        self.assertEqual(db, samedb, msg="THE DATABASES WERE NOT EQUAL")
        os.remove('test_db_to_file_to_db.txt')

    def test_db_to_file_to_db_duplicates(self):
        db = {'a': {'aa': 'abcd', 'bb': 'bcde', 'cc': 'fghi'},
              'b': {'aa': 'efgh', 'bb': 'fghi', 'cc': 'fghi'},
              'c': {'aa': 'ijkl', 'bb': 'jklm', 'cc': 'fghi'},
              'd': {'aa': 'mnop', 'bb': 'nopq', 'cc': 'fghi'}}
        db_to_file(db, 'test_db_to_file_to_db_duplicates.txt')

        duplicate_db = {'b': {'aa': 'efgh', 'bb': 'fghi', 'cc': 'fghi'}}
        with open('test_db_to_file_to_db_duplicates.txt', 'a') as f:
            json.dump(duplicate_db, f)
            f.write('\n')
        samedb = file_to_db('test_db_to_file_to_db_duplicates.txt')
        self.assertEqual(db, samedb, msg="THE DATABASES WERE NOT EQUAL")
        os.remove('test_db_to_file_to_db_duplicates.txt')

    def test_check_if_db_is_in_file(self):
        first = {'header001': {'type': 'container vessel', 'callsign': 'br"olt', 'length': 14.114, 'width': 7.11}}
        frist = {'header001': {'callsign': 'br"olt', 'length': 14.114, 'width': 7.11, 'type': 'container vessel'}}
        not_in_db = {'header005': {'callsign': 'br"olt', 'length': 14.114, 'width': 7.11, 'type': 'container vessel'}}
        self.assertTrue(check_if_db_is_in_file(first, 'test_jsonDict_to_file.txt'),
                        msg="DIDN'T FIND THE FIRST DATABASE")
        self.assertTrue(check_if_db_is_in_file(frist, 'test_jsonDict_to_file.txt'),
                        msg="DIDN'T FIND THE FRIST DATABASE")
        self.assertFalse(check_if_db_is_in_file(not_in_db, 'test_jsonDict_to_file.txt'),
                        msg="FOUND A NON EXISTING DICT IN DB FILE")

    def test_add_dict_to_file(self):
        pass

    def test_groom_file_db(self):
        db = {'a': {'aa': 'abcd', 'bb': 'bcde', 'cc': 'fghi'},
              'b': {'aa': 'efgh', 'bb': 'fghi', 'cc': 'fghi'},
              'c': {'aa': 'ijkl', 'bb': 'jklm', 'cc': 'fghi'},
              'd': {'aa': 'mnop', 'bb': 'nopq', 'cc': 'fghi'}}

        db_to_file(db, 'test_groom_file_db_inFile.txt')
        duplicate1_db = {'b': {'aa': 'efgh', 'bb': 'fghi', 'cc': 'fghi'}}
        duplicate2_db = {'c': {'aa': 'ijkl', 'bb': 'jklm', 'cc': 'fghi'}}

        with open('test_groom_file_db_inFile.txt', 'a') as f:
            json.dump(duplicate1_db, f)
            f.write('\n')
            json.dump(duplicate1_db, f)
            f.write('\n')
            json.dump(duplicate1_db, f)
            f.write('\n')
            json.dump(duplicate2_db, f)
            f.write('\n')

        groom_file_db('test_groom_file_db_inFile.txt', 'test_groom_file_db_outFile.txt')

        db2 = file_to_db('test_groom_file_db_outFile.txt')
        self.assertEqual(db, db2, msg="THE DATABASES ARE NOT EQUAL")
        os.remove('test_groom_file_db_inFile.txt')
        os.remove('test_groom_file_db_outFile.txt')

    def tearDown(self):
        os.remove('test_jsonDict_to_file.txt')

if __name__ == '__main__':
    unittest.main()
