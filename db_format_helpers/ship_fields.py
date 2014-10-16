__author__ = 'thorsteinn'


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
    except ValueError:
        return False
    except TypeError:
        return False

def is_int(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    except TypeError:
        return False
    else:
        return a == b


def stringnumbers_to_numbers(db):
    ships = db.keys()
    for ship in ships:
        ship_db = db[ship]
        fields = ship_db.keys()
        for field in fields:
            if ship_db[field]:      # Checks to make sure the field value is not None
                if is_number(ship_db[field]):
                    if is_int(ship_db[field]):
                        ship_db[field] = int(ship_db[field])
                    else:
                        ship_db[field] = float(ship_db[field])


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
