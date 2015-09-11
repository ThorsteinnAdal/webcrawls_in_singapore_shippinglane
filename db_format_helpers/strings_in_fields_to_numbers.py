__author__ = 'thorsteinn'
from is_number import is_number
from is_int import is_int

def strings_in_fields_to_numbers(db_key, db):
    """
    A method for converting typed numbers to actual numbers
    u'123.22' should be turned into a floating point number
    u'123' should be turned into an integer number
    :param db_key: specifies individual key that should be processed. If left blank, all fields in the db are processed
    :param db: a db that is processed
    :return: the script changes the db that is passed to it
    """
    ships = db.keys()
    for ship in ships:
        ship_db = db[ship]
        if type(db_key) is list:
            fields = db_key
        else:
            if db_key:
                fields = [db_key]
                if db_key.lower() == 'all' or db_key is None:
                    fields = ship_db.keys()
            else:
                raise KeyError('{this_key} is not recognized as a valid key.'.format(this_key=db_key))

        for field in fields:
            if field in ship_db.keys() and ship_db[field] and is_number(ship_db[field]):
                val = str(ship_db[field])
                if val.upper() != 'INFINITY':
                    if ',' in val:
                        val = str(ship_db[field]).replace(',', '')
                    if '.' in val:
                        ship_db[field] = float(val)
                    else:
                        ship_db[field] = int(val)

