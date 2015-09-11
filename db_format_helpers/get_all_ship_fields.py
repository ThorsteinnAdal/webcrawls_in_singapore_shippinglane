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
