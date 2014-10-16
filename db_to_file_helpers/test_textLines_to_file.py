__author__ = 'thorsteinn'

import unittest

from textLines_to_file import line_in_file, remove_line_from_file, add_unique_line_to_file

class Test_textLines_to_file(unittest.TestCase):
    def setUp(self):
        with open('unit_test_file.txt','w') as f:
            f.write('this is the first line\n')
            f.write('this line is repeated twice\n')
            f.write('\n')
            f.write('this line is repeated twice\n')
            f.write('this line \"has quotation marks\"\n')
            f.write('this is the last line\n')

    def test_line_in_file(self):
        self.assertTrue(line_in_file('this is the first line', 'unit_test_file.txt'), msg='FIRST LINE NOT FOUND')
        self.assertTrue(line_in_file('this is the last line', 'unit_test_file.txt'), msg='LAST LINE NOT FOUND')
        self.assertFalse(line_in_file('this line should not be found', 'unit_test_file.txt'), msg="A LINE THAT WASN'T THERE WAS FOUND")
        self.assertTrue(line_in_file('', 'unit_test_file.txt'), msg="A BLANK WAS FOUND")
        self.assertTrue(line_in_file('\n', 'unit_test_file.txt'), msg="A SIMPLE RETURN FAILED")

    def test_remove_line_from_file(self):
        self.setUp()
        self.assertFalse(remove_line_from_file('this line is not in the file', 'unit_test_file.txt'), msg = "A LINE WAS REMOVED THAT DIDNT EXIST")
        self.assertTrue(remove_line_from_file('this is the first line', 'unit_test_file.txt'), msg="THE FIRST LINE WAS NOT REMOVED")
        self.assertFalse(remove_line_from_file('this is the first line', 'unit_test_file.txt'), msg="THE FIRST LINE WAS REMOVED TWICE")
        self.assertTrue(remove_line_from_file('this is the last line', 'unit_test_file.txt'), msg="FAILED TO REMOVE THE LAST LINE")
        self.assertTrue(remove_line_from_file('this line is repeated twice', 'unit_test_file.txt'), msg="A DUPLICATED LINE WAS NOT REMOVED")
        self.assertTrue(remove_line_from_file('this line is repeated twice', 'unit_test_file.txt'), msg="THE SECOND DUPLICATED LINE WAS NOT REMOVED")

    def test_add_unique_line_to_file(self):
        with open('unit_test_file.txt', 'r') as f:
            fl1 = len(f.read())
        self.assertTrue(add_unique_line_to_file('a new line that is added', 'unit_test_file.txt'), msg="FAILED TO ADD A NEW LINE TO THE FILE")
        with open('unit_test_file.txt', 'r') as f:
            fl2 = len(f.read())
        self.assertEqual(fl1+len('a new line that is added\n'), fl2, msg="THE RESULTING FILE IS OF INCORRECT LENGTH")

        self.assertFalse(add_unique_line_to_file('a new line that is added', 'unit_test_file.txt'), msg="ADDED A NEW LINE TWICE TO THE FILE")
        with open('unit_test_file.txt', 'r') as f:
            fl3 = len(f.read())
        self.assertEqual(fl2, fl3, msg="THE RESULTING FILE IS OF INCORRECT LENGTH WHEN NOTHING WAS TO BE ADDED")

        self.assertFalse(add_unique_line_to_file('this is the last line', 'unit_test_file.txt'), msg="ADDED A PRE-EXISTING LINE")


    def tearDown(self):
        import os
        os.remove('unit_test_file.txt')


def runTests():
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_JSON_to_file)
    unittest.TextTestRunner(verbosity=2).run(suite)



if __name__ == '__main__':
    unittest.main()
