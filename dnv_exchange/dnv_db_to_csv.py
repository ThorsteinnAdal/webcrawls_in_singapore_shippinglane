__author__ = 'thorsteinn'

from db_to_file_helpers.jsonDicts_to_file import file_to_db
from db_format_helpers.ship_fields import get_all_ship_fields
import unicodecsv
import reformat_dnv_file


def parse_component_name(s):
    """
    A script for parsing dnv-engine information. Possible engine components were extracted by visual inspection
    of all fields seen in the dnv-machinery database
    :param s: the dnv name of a machine component
    :return: a tuple with four values, machinery type, sub-type, comments and original string
    """
    machineryType = None
    machinerySub = None
    remains = s[:]

    auxiliary_sub_sub_class = ['composite', 'electric heated', 'exhaust gas heated', 'oil/gas fired']
    auxiliary_steam_generator_sub_class = []
    emergency_generator_sub_class = ['diesel engine']
    intermediate_shaft_sub_class = []
    main_generator_sub_class = ['diesel engine', 'driver', 'gas turbine arrangement', 'power take off',
                                'power take off/Propulsion reduction gear power take off', 'steam turbine']
    mar_sub_class = []
    maneuvring_thruster_sub_class = ['azimuth', 'diesel engine', 'electric motor', 'electric power unit',
                                     'hydraulic motor', 'pump jet', 'tunnel']

    propeller_sub_class = ['controllable pitch', 'fixed built', 'mono-block', 'shaft arrangement', ]

    propulsion_sub_class = ['boiler - oil/gas fired', 'diesel engine', 'driver', 'electric power unit',
                            'pod, azimuth', 'reduction gear', 'retractable azimuth thruster arrangement',
                            'steam turbine']
    pwv_sub_class = []
    steering_gear_sub_class = []
    propulsion_thruster_sub_class = ['azimuth', 'cycloidal',
                            'diesel engine', 'driver', 'electric motor',
                            'electric power unit', 'gas turbine arrangement',
                            'hydraulic motor', 'intermediate shaft', 'reduction gear']
    thermal_oil_heater_sub_class = ['exhaust heated', 'oil fired', 'steam heated']

    machinery_dict = {'Auxiliary boiler': auxiliary_sub_sub_class,
                         'Auxiliary steam generator': auxiliary_steam_generator_sub_class,
                         'Emergency generator': emergency_generator_sub_class,
                         'Intermediate shaft': intermediate_shaft_sub_class,
                         'Main generator': main_generator_sub_class,
                         'Manoeuvring retractable azimuth thruster arrangement': mar_sub_class,
                         'Manoeuvring thruster': maneuvring_thruster_sub_class,
                         'Propeller': propeller_sub_class,
                         'Propulsion': propulsion_sub_class,
                         'Propulsion thruster': propulsion_thruster_sub_class,
                         'Propulsion waterjet, variable': pwv_sub_class,
                         'Steering gear': steering_gear_sub_class,
                         'Thermal oil heater': thermal_oil_heater_sub_class}

    match_keys = machinery_dict.keys()

    for mk in match_keys:
        if remains.find(mk) == 0:
            machineryType = mk
            remains = remains.replace(mk,'').strip()
            if len(remains) == 0:
                remains = None
                break
            else:
                for st in machinery_dict[mk]:
                    if len(st) is not 0:
                        if st in s:
                            machinerySub = st
                            remains = remains.replace(st, '').strip()
                            break
                        else:
                            machinerySub = None
                break
        else:
            machineryType = None

    if remains and remains[0] == ',':
        remains = remains[1:].strip()

    return machineryType, machinerySub, remains, s


def dnv_db_extract_engine_db(db, **kwargs):
    """
    A method for extracting a machinery table information from a dnv_db object.
    :param db: a database object of the type {ship1:{ship database},ship2:{ship database}
    one of the database keys should point to a table of machinery objects according to dnv-exchange
    :param kwargs: optinal arguments for controlling output and for tweaking which key is used
    :returns: The method returns csv file or txt file if requested.
                if the output file is None, a db object is returned
    """
    table_key = kwargs.pop('machinery_table_key', 'machinery_l')
    output_file = kwargs.pop('output_file', 'dnv_engines.csv')

    from db_to_file_helpers.jsonDicts_to_file import dump_db_to_csv, db_to_file
    ships = db.keys()

    engine_db = {}
    for ship in ships:
        ship_db = db[ship]
        if table_key in ship_db.keys():
            ship_engine_table = ship_db[table_key]
            if 'imo_id' in ship_db.keys():
                id_name = 'imo_id'
                ship_id = ship_db['imo_id']
            else:
                id_name = 'dnv_id'
                ship_id = ship_db['dnv_id']

            counter = 0
            for line in ship_engine_table:
                entry_name = 'entry'+str(ship_id) + '-' + str(counter)
                component_name = parse_component_name(line[0]) if line[0] else None
                product_name = line[1] if line[1] else None
                designer_name = line[2] if line[2] else None
                if counter:
                    engine_db[entry_name] = {id_name: ship_id,
                                             'engine_id': counter,
                                             'component_role_s': component_name[0],
                                             'component_class_s': component_name[1],
                                             'component_comments_s': component_name[2],
                                             'product_s': product_name,
                                             'designer_s': designer_name}
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


def dnv_db_to_csv(db, **kwargs):
    """
    A script for generating a csv file from a dnv-db object. The script removes selected fields from the db
    and does some minor grooming of the db
    :param db: a standard db object: {ship1:{ship1_db}, ship2:{ship2_db}}
    :**kwargs: additional arguments
    :return:
    """
    from db_to_file_helpers.jsonDicts_to_file import dump_db_to_csv

    output_file = kwargs.pop('output_file', 'dnv_db.csv')
    dnv_type_s = kwargs.pop('dnv_type_s', 'dnv_type_s')
    del_list = kwargs.pop('del_list', ['machinery_l'])
    if type(del_list) is not list:
        del_list = [del_list]

    ships = db.keys()
    for ship in ships:
        ship_db = db[ship]
        if dnv_type_s in ship_db.keys():
            old_dnv_type = ship_db[dnv_type_s]
            dnv_type_number = old_dnv_type[:3]
            dnv_type_text = old_dnv_type[6:]
            ship_db['dnv_type_n'] = int(dnv_type_number)
            ship_db['dnv_type_tx_s'] = dnv_type_text
            del (ship_db[dnv_type_s])
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
        dnv_db_to_csv(db, output_file=ship_db_output_csv, dnv_type_s='dnv_type_s', del_list=['machinery_l'])


if __name__ == '__main__':
    main('./dnv_exchange_gets/dnv_db_fixed.txt', 'dnv_db.csv', 'dnv_engines.csv')