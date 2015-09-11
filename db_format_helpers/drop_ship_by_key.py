__author__ = 'thorsteinn'


def drop_ships_by_key_value(key_to_check, value_to_check, db):
    """
    Steady method for dropping db entries using a key:value requirement
    :param key_to_check:
    :param value_to_check:
    :param db:
    :return: alters the db in place
    """
    ships = db.keys()
    for ship in ships:
        ship_db = db[ship]
        if ship_db[key_to_check] is value_to_check:
            del(db[ship])
