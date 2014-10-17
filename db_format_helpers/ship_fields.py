__author__ = 'thorsteinn'

from db_format_helpers import get_all_ship_fields

def get_all_ship_fields(db):
    ships = db.keys()
    fields = []
    for ship in ships:
        shipDB = db[ship]
        shipKeys = shipDB.keys()
        for oneKey in shipKeys:
            if oneKey not in fields:
                fields.append(oneKey)

    return fields


def rename_ship_field(old_name, new_name, db):
    ships = db.keys()
    outputDB = {}
    for ship in ships:
        shipDB = db[ship]
        if old_name in shipDB.keys():
            shipDB[new_name] = shipDB.pop(old_name)

        outputDB[ship] = shipDB

    return outputDB


def is_number(s):
    try:
        float(s)
        return True
    except ValueError, me:
        if len(s.replace(',', ''))< len(s):
            return is_number(s.replace(',', ''))
        return False
    except TypeError, me:
        return False
    except AttributeError, me:
        return False


def is_int(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    except TypeError:
        return False
    except AttributeError:
        return False
    else:
        return a == b

def stringnumbers_to_numbers(db_key, db):
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
        if db_key:
            fields = [db_key]
        else:
            fields = ship_db.keys()

        for field in fields:
            if field in ship_db.keys() and ship_db[field] and is_number(ship_db[field]):
                if is_int(ship_db[field].replace(',', '')):
                    ship_db[field] = int(ship_db[field].replace(',', ''))
                else:
                    ship_db[field] = float(ship_db[field].replace(',', ''))


def replace_blanks_in_db(db_key, new_value, db):
    ships = db.keys()
    for ship in ships:
        ship_db = db[ship]
        if db_key:
            fields = [db_key]
        else:
            fields = ship_db.keys()

        for field in fields:
            if field in ship_db.keys() and len(ship_db[field].strip()) == 0:
                ship_db[field] = new_value


def drop_ships_by_key_value(key_to_check, value_to_check, db):
    ships = db.keys()
    for ship in ships:
        ship_db = db[ship]
        if ship_db[key_to_check] == value_to_check:
            del(db[ship])


def list_all_field_values(key_to_check, db):
    ships = db.keys()
    returnList = []
    for ship in ships:
        ship_db = db[ship]
        if key_to_check in ship_db.keys():
            returnList.append(ship_db[key_to_check])
    return returnList


def empty_to_null(key_to_check, db):
    return None