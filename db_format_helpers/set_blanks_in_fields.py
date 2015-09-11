__author__ = 'thorsteinn'


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
