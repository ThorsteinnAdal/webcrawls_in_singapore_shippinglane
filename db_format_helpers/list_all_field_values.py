__author__ = 'thorsteinn'


def list_all_field_values(key_to_check, db):
    ships = db.keys()
    returnList = []
    for ship in ships:
        ship_db = db[ship]
        if key_to_check in ship_db.keys():
            returnList.append(ship_db[key_to_check])
    return returnList
