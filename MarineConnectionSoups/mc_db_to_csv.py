__author__ = 'thorsteinn'

from db_to_file_helpers.jsonDicts_to_file import file_to_db


def mc_db_extract_subtable_db(db, **kwargs):
    """
    A method for extracting a sub-table information from a mc-db object.
    :param db: a database object of the type {ship1:{ship database},ship2:{ship database}
    one of the database keys should point to a table of machinery objects according to dnv-exchange
    :param kwargs: optinal arguments for controlling output and for tweaking which key is used
    :returns: The method returns csv file or txt file if requested.
                if the output file is None, a db object is returned
    """
    table_key = kwargs.pop('table_key', 'former_names_l')
    output_file = kwargs.pop('output_file', 'mc_former_names.csv')

    from db_to_file_helpers.jsonDicts_to_file import dump_db_to_csv, db_to_file
    ships = db.keys()

    work_db = {}
    for ship in ships:
        ship_db = db[ship]
        if table_key in ship_db.keys():
            the_table = ship_db[table_key]
            if 'imo_id' in ship_db.keys():
                id_name = 'imo_id'
                ship_id = ship_db['imo_id']
            else:
                id_name = 'mmsi_id'
                ship_id = ship_db['mmsi_id']

            counter = 0
            for line in the_table:
                entry_name = 'entry'+str(ship_id) + '-' + str(counter)
                product_name = line[1] if line[1] else None
                designer_name = line[2] if line[2] else None
                if counter:
                    pass
                counter += 1

    if output_file:
        file_type = output_file.split('.')[-1]
        if file_type.lower() =='csv':
            dump_db_to_csv(engine_db, output_file)
            print 'From "dnv_db_extract_engine_db", ouput: %s generated' % output_file
            return None
        else:
            db_to_file(db, output_file)
    else:
        return engine_db


def mc_db_to_csv(db, **kwargs):
    """
    A script for generating a csv file from a mc-db object. The script removes selected fields from the db
    and does some minor grooming of the db
    :param db: a standard db object: {ship1:{ship1_db}, ship2:{ship2_db}}
    :**kwargs: additional arguments
    :return:
    """
    from db_to_file_helpers.jsonDicts_to_file import dump_db_to_csv

    output_file = kwargs.pop('output_file', 'mc_db.csv')
    del_list = kwargs.pop('del_list', ['former_names_l'])
    if type(del_list) is not list:
        del_list = [del_list]

    ships = db.keys()
    for ship in ships:
        ship_db = db[ship]
        for to_delete in del_list:
            if to_delete in ship_db.keys():
                del (ship_db[to_delete])

    if output_file:
        dump_db_to_csv(db, output_file)
        print 'From "dnv_db_to_csv", ouput: %s generated' % output_file
        return None
    else:
        return db


def main(db_input_file, ship_db_output_csv, engine_db_output_csv):

    if engine_db_output_csv:
        db = file_to_db(db_input_file)
        dnv_db_extract_engine_db(db, output_file=engine_db_output_csv, machinery_table_key='machinery_l')

    if ship_db_output_csv:
        db = file_to_db(db_input_file)
        mc_db_to_csv(db, output_file=ship_db_output_csv, del_list=['former_names_l'])


if __name__ == '__main__':
    main('./all_get_db_masters/mc_db_master.txt', 'mc_db.csv', None)