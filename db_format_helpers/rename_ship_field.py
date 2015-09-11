__author__ = 'thorsteinn'


def rename_ship_field(old_name, new_name, db):
    ships = db.keys()
    outputDB = {}
    for ship in ships:
        shipDB = db[ship]
        if old_name in shipDB.keys():
            shipDB[new_name] = shipDB.pop(old_name)

        outputDB[ship] = shipDB

    return outputDB