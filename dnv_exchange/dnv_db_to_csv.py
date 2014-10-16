__author__ = 'thorsteinn'

from db_to_file_helpers.jsonDicts_to_file import file_to_db
from db_format_helpers.ship_fields import get_all_ship_fields
import unicodecsv


def parse_component_name(s):
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



def dnv_db_extract_engine_db(db, output_file):
    ships = db.keys()

    engine_db = {}
    for ship in ships:
        ship_db = db[ship]
        if 'machinery_l' in ship_db.keys():
            ship_engine_table = ship_db['machinery_l']
            shipID = ship_db['imo_id']
            counter = 0
            for line in ship_engine_table:
                entry_name = ship + '-' + str(counter)
                component_name = parse_component_name(line[0]) if line[0] else ''
                product_name = line[1] if line[1] else ''
                designer_name = line[2] if line[2] else ''
                if counter:
                    engine_db[entry_name] = {'imo_id': shipID,
                                             'engine_id': counter,
                                             'component_role_s': component_name[0],
                                             'component_class_s': component_name[1],
                                             'component_comments_s': component_name[2],
                                             'product_s': product_name,
                                             'designer_s': designer_name}
                counter += 1
    if output_file:
        all_fields = get_all_ship_fields(engine_db)
        all_engines = engine_db.keys()
        with open(output_file, 'w') as f:
            csv_output = unicodecsv.DictWriter(f, all_fields, encoding='utf-8')
            csv_output.writeheader()
            for engine in all_engines:
                db_row = engine_db[engine]
                csv_output.writerow(db_row)
        print 'From "dnv_db_extract_engine_db", ouput: %s generated' % output_file


db = file_to_db('../output_files/dnv_db_get_1_fixed.txt')
dnv_db_extract_engine_db(db, 'dnv_engines.csv')


def dnv_db_to_csv(db, output_file):
    ships = db.keys()
    for ship in ships:
        ship_db = db[ship]
        if 'dnv_type_s' in ship_db.keys():
            old_dnv_type = ship_db['dnv_type_s']
            dnv_type_number = old_dnv_type[:3]
            dnv_type_text = old_dnv_type[6:]
            ship_db['dnv_type_n'] = int(dnv_type_number)
            ship_db['dnv_type_tx_s'] = dnv_type_text
            del (ship_db['dnv_type_s'])
        if 'machinery_l' in ship_db.keys():
            del (ship_db['machinery_l'])

    if output_file:
        all_fields = get_all_ship_fields(db)
        with open(output_file, 'w') as f:
            csv_output = unicodecsv.DictWriter(f, all_fields, encoding='utf-8')
            csv_output.writeheader()
            for ship in ships:
                ship_db = db[ship]
                csv_output.writerow(ship_db)
        print 'From "dnv_db_to_csv", ouput: %s generated' % output_file

'''
db = file_to_db('../output_files/dnv_db_get_1_fixed.txt')
dnv_db_to_csv(db, 'dnv_db.csv')

'''