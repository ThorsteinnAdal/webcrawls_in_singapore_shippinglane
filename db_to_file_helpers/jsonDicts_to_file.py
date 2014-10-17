__author__ = 'thorsteinn'

import json


def file_to_db(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        db = {}
        for line in lines:
            oneDict = json.loads(line.strip())
            db.update(oneDict)  # here duplicate entries will be thrown out
        return db


def db_to_file(db, file_name):
    db_keys = db.keys()
    to_file = {}
    with open(file_name, 'w') as f:
        for one_db in db_keys:
            to_file[one_db] = db[one_db]
            json.dump(to_file, f)
            f.write('\n')
            to_file = {}


def check_if_db_is_in_file(dict, file_name):
    dict_key = dict.keys()
    db = file_to_db(file_name)
    db_keys = db.keys()
    if unicode(dict_key[0]) in db_keys:
        return True
    else:
        return False


def append_db_to_file(dict, file_name):
    with open(file_name, 'a') as f:
        json.dump(dict,f)
        f.write('\n')


def groom_file_db(old_file, new_file):
    """
    A turn-over method that should remove duplicates from databases. May have some unforeseen consequences
    :param old_file: An old file containing a database
    :param new_file: A new file that is created, may be the same as the old file
    :return:
    """
    db = file_to_db(old_file)
    db_to_file(db, new_file)


def dump_db_to_csv(db, output_file):
    import unicodecsv
    from db_format_helpers.ship_fields import get_all_ship_fields

    all_fields = get_all_ship_fields(db)
    all_rows = db.keys()
    with open(output_file, 'w') as f:
        csv_output = unicodecsv.DictWriter(f, all_fields, encoding='utf-8')
        csv_output.writeheader()
        try:
            for row in all_rows:
                to_write = db[row]
                csv_output.writerow(to_write)
            return True
        except Exception, me:
            print me.message
            return False


