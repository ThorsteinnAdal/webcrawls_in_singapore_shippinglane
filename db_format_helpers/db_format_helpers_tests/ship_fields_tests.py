__author__ = 'thorsteinn'

import unittest
import ship_fields


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
                 u'all_same_id': u'000011'},
            'ship2':
                {u'name_s': 'SHIP 2',
                 u'machine_l': [[u'name', u'role', u'power', u'note'],
                                [u'Propulsion', u'Wartsilla', u'7800'],
                                [u'Aux', u'Volvo', u'30.115']],
                 u'length_f': u'41.115',
                 u'imo_id': u'',
                 u'dnv_id': u'12345678',
                 u'all_have_this_id': u'234',
                 u'all_same_id': u'000011'},
            'ship3':
                {u'name_s': 'SHIP 3',
                 u'machine_l': [[u'name', u'role', u'power', u'note'],
                                [u'Propulsion', u'Volvo', u'800.15'],
                                [u'Aux', u'Cat', u'315']],
                 u'length_f': u'1,225',
                 u'imo_id': u'98765432',
                 u'dnv_id': u'',
                 u'all_have_this_id': u'456',
                 u'all_same_id': u'000011'},
        }
        return db

    def test_get_all_ship_fields(self):
        known_fields = ['name_s', 'machine_l', 'length_f', 'imo_id', 'dnv_id', 'extra']
        db = self.set_up_db()
        fields_in_db = ship_fields.get_all_ship_fields(db)
        self.assertEqual(len(fields_in_db), 7,
                         msg='Obtained the incorrect number of expected 7 but got %s' % len(fields_in_db))
        for field in fields_in_db:
            if field in known_fields:
                pre = len(known_fields)
                known_fields.remove(field)
                self.assertEquals(pre - 1, len(known_fields))


    def test_rename_ship_field(self):
        db = self.set_up_db()
        old_fields = ship_fields.get_all_ship_fields(db)
        ship_fields.rename_ship_field('name_s', 'name', db)
        new_fields = ship_fields.get_all_ship_fields(db)
        self.assertTrue('name_s' in old_fields)
        self.assertFalse('name' in old_fields)
        self.assertTrue('name' in new_fields)
        self.assertFalse('name_s' in new_fields)


    def test_is_number(self):
        self.assertTrue(ship_fields.is_number(1), msg="Found that 1 is not a number")
        self.assertTrue(ship_fields.is_number(1.1254))
        self.assertTrue(ship_fields.is_number('3'))
        self.assertTrue(ship_fields.is_number(u'1.1254'))
        self.assertFalse(ship_fields.is_number(u'd1.1254'))
        self.assertFalse(ship_fields.is_number(['1,1254']))
        self.assertFalse(ship_fields.is_number([1.1254]))


    def test_is_int(self):
        self.assertTrue(ship_fields.is_int(100))
        self.assertTrue(ship_fields.is_int(100.0))
        self.assertTrue(ship_fields.is_int('100'))
        self.assertTrue(ship_fields.is_int('100.0'))
        self.assertFalse(ship_fields.is_int(100.1))
        self.assertFalse(ship_fields.is_int('100.1'))
        self.assertFalse(ship_fields.is_int('d100.1'))
        self.assertFalse(ship_fields.is_int([100.1]))


    def test_list_all_field_values(self):
        db = self.set_up_db()
        haul = ship_fields.list_all_field_values('name_s', db)
        self.assertEquals(len(haul), 3)
        self.assertTrue('SHIP 1' in haul)
        haul = ship_fields.list_all_field_values('length_f', db)
        self.assertEquals(len(haul), 3)
        haul = ship_fields.list_all_field_values('imo_id', db)
        self.assertEquals(len(haul), 3)
        haul = ship_fields.list_all_field_values('dnv_id', db)
        self.assertEquals(len(haul), 3)

    def test_stringnumbers_to_numbers(self):
        db = self.set_up_db()
        haul = ship_fields.list_all_field_values('all_have_this_id', db)
        for val in haul:
            self.assertTrue(ship_fields.is_int(val))

        ship_fields.stringnumbers_to_numbers('all_have_this_id', db)
        haul = ship_fields.list_all_field_values('all_have_this_id', db)
        for val in haul:
            self.assertTrue(ship_fields.is_int(val))
        ship_fields.stringnumbers_to_numbers('all_same_id', db)

        haul = ship_fields.list_all_field_values('all_same_id', db)
        for val in haul:
            self.assertTrue(ship_fields.is_int(val))

        ship_fields.stringnumbers_to_numbers('all_have_this_id', db)
        haul = ship_fields.list_all_field_values('all_have_this_id', db)
        for val in haul:
            self.assertTrue(ship_fields.is_int(val))
        ship_fields.stringnumbers_to_numbers('all_same_id', db)

        haul = ship_fields.list_all_field_values('not_found', db)
        self.assertEqual(len(haul), 0, msg='Expected length to be 0, got length %s' % len(haul))
        ship_fields.stringnumbers_to_numbers('not_found', db)

        haul = ship_fields.list_all_field_values('length_f', db)
        for val in haul:
            self.assertTrue(ship_fields.is_number(val), msg='The value %s is not a valid number' % str(val))

        ship_fields.stringnumbers_to_numbers(None, db)
        haul = ship_fields.list_all_field_values('length_f', db)
        for val in haul:
            self.assertTrue(ship_fields.is_number(val), msg='The value %s is not a valid number' % str(val))


    def test_drop_ships_by_key_value(self):
        db = self.set_up_db()
        ships = db.keys()
        self.assertTrue('ship2' in ships, msg="Didn't find ship2 in the database, incorrect initialization")

        ship_fields.drop_ships_by_key_value('imo_id', '', db)
        ships = db.keys()
        self.assertFalse('ship2' in ships, msg="ship2 still in the database, didn't drop the ship by imo_id")
        self.assertTrue('ship1' in ships, msg="ship1 was dropped by imo_id key when it shouldn't have")
        self.assertTrue('ship3' in ships, msg="ship3 was dropped by imo_id key when it shouldn't have")

        ship_fields.stringnumbers_to_numbers(None, db)
        ship_fields.drop_ships_by_key_value('dnv_id', u'', db)
        ships = db.keys()
        self.assertFalse('ship3' in ships, msg="ship3 was not dropped by dnv_id key when it should have")
        self.assertTrue('ship1' in ships, msg="ship1 was dropped by dnv_id key when it shouldn't have")

        ship_fields.drop_ships_by_key_value('name_s', 'SOME SHIP', db)
        ships = db.keys()
        self.assertTrue('ship1' in ships)

        ship_fields.drop_ships_by_key_value('name_s', 'SHIP 1', db)
        ships = db.keys()
        self.assertTrue('ship1' not in ships)

        db = self.set_up_db()
        ships = db.keys()
        self.assertTrue('ship1' in ships, msg="Didn't find ship1 in the database, incorrect initialization")
        ship_fields.stringnumbers_to_numbers('all_have_this_id', db)
        ship_fields.drop_ships_by_key_value('all_have_this_id', '123', db)
        ships = db.keys()
        self.assertTrue('ship1' in ships)
        ship_fields.drop_ships_by_key_value('all_have_this_id', 123, db)
        ships = db.keys()
        self.assertFalse('ship1' in ships)
        self.assertTrue('ship2' in ships)
        ship_fields.drop_ships_by_key_value('dnv_id', 12345678, db)
        ships = db.keys()
        self.assertTrue('ship2' in ships)
        ship_fields.drop_ships_by_key_value('dnv_id', '12345678', db)
        ships = db.keys()
        self.assertFalse('ship2' in ships)


    def test_replace_blanks_in_db(self):
        db = self.set_up_db()
        haul = ship_fields.list_all_field_values('dnv_id', db)
        self.assertEqual(len(haul), 3)
        ship_fields.replace_blanks_in_db('dnv_id', None, db)
        haul = ship_fields.list_all_field_values('dnv_id', db)
        self.assertEqual(len(haul), 2)


if __name__ == '__main__':
    unittest.main()
