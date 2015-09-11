__author__ = 'thorsteinn'

def check_field_values(key_id, db, **kwargs):
    if len(kwargs) > 1:
        raise KeyError("Only one keyword is allowed to be used at a time. Received {length!s} arguments."
                       "\n {kwargs}".format(length=len(kwargs), kwargs=kwargs))
    has_all_numbers = kwargs.pop('has_all_numbers', False)
    has_all_blanks = kwargs.pop('has_all_blanks', False)
    has_all_text = kwargs.pop('has_all_text', False)
    has_no_blanks = kwargs.pop('has_no_blanks', False)
    has_blanks = kwargs.pop('has_blanks', False)


    if has_blanks and has_all_blanks and has_no_blanks and has_all_numbers and has_all_text is False:
        raise KeyError("One keyword must be set to true")

    ships = db.keys()
    sw = False
    for ship in ships:
        ship_db = db[ship]
        if key_id in ship_db.keys():
            val_type = type(ship_db[key_id])

            if has_all_numbers:
                if val_type is int or val_type is float:
                    sw = True
                else:
                    return False

            if has_all_blanks is True:
                if val_type is str or val_type is unicode:
                    if len(ship_db[key_id].strip()) is 0:
                        sw = True
                    else:
                        return False

            if has_all_text is True:
                if val_type is str or val_type is unicode:
                    sw = True
                else:
                    return False

            if has_no_blanks is True:
                sw = True
                if ship_db[key_id] is None:
                    return False
                if val_type is str or val_type is unicode:
                    if len(ship_db[key_id].strip()) is 0:
                        return False

            if has_blanks is True:
                sw = False
                if ship_db[key_id] is None:
                    return True
                elif val_type is str or val_type is unicode:
                    if len(ship_db[key_id].strip()) is 0:
                        return True
                else:
                    pass

    return sw