__author__ = 'thorsteinn'


def set_blanks_to_None(key_id, db, trailing_blanks=False):
    ships = db.keys()
    for ship in ships:
        ship_db = db[ship]

        if key_id.lower() == 'all' or key_id is None:
            fields = ship_db.keys()
        else:
            if type(key_id) is list:
                fields = key_id
            else:
                fields = [key_id]

        for field in fields:
            if field in ship_db.keys():
                val_type = type(ship_db[field])
                if val_type is str or val_type is unicode:
                    if len(ship_db[field].strip()) is 0:
                        ship_db[field] = None
                    if trailing_blanks is True:
                        if ship_db[field] is not None:
                            ship_db[field] = ship_db[field].strip()
