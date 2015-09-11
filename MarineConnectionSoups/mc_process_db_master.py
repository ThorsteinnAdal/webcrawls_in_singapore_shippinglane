__author__ = 'thorsteinn'


from db_to_file_helpers.jsonDicts_to_file import file_to_db, db_to_file
from db_format_helpers.strings_in_fields_to_numbers import strings_in_fields_to_numbers
import os
from db_format_helpers.set_blanks_to_None import set_blanks_to_None
from db_format_helpers.drop_ship_by_key import drop_ships_by_key_value
from db_format_helpers.get_all_ship_fields import get_all_ship_fields
from db_format_helpers.rename_ship_field import rename_ship_field

def mc_process_db_master(db_input_file, **kwargs):

###### setup segment
    if os.path.isfile(db_input_file) is False:
        print "Select an existing db file"
        return False
    else:
        work_folder = os.path.dirname(db_input_file)
        input_file_name = os.path.basename(db_input_file)
        input_file_n = os.path.splitext(input_file_name)[0]
    try:
        db = file_to_db(db_input_file)
    except Exception, me:
        print me.message
        return False

    if 'output_file' in kwargs.keys():
        output_file = kwargs.pop('output_file')
    else:
        output_file = os.path.join(work_folder, input_file_n + '_fix.txt')

###### end of setup segment

    print "setting input to {input_file}, setting output to {output_file}".format(input_file=db_input_file, output_file=output_file)

###### processing data-fields

    rename_ship_field('Name of the ship', 'name_s', db)
    rename_ship_field('DWT', 'dwt_n', db)
    rename_ship_field('Former names', 'former_names_l', db)
    rename_ship_field('Gross tonnage', 'gt_n', db)
    rename_ship_field('MMSI', 'mmsi_id', db)
    rename_ship_field('Year of build', 'build_year_n', db)
    rename_ship_field('Manager & owner', 'manager_owner_s', db)
    rename_ship_field('Flag', 'ship_flag_s', db)
    rename_ship_field('Class society', 'classificaion_society_s', db)
    rename_ship_field('Type of ship', 'ship_type_s', db)
    rename_ship_field('Home port', 'port_of_registry_s', db)
    rename_ship_field('IMO number', 'imo_id', db)
    rename_ship_field('Manager', 'manager_s', db)
    rename_ship_field('Owner', 'owner_s', db)
    rename_ship_field('Last known flag', 'last_flag_s', db)
    rename_ship_field('Name of ship', 'name_s', db)
    rename_ship_field('Builder', 'yard_s', db)

    drop_ships_by_key_value("name_s", None, db)
    strings_in_fields_to_numbers('all', db)
    set_blanks_to_None('all', db, trailing_blanks=True)

    db_to_file(db, output_file)

if __name__ == "__main__":
    mc_process_db_master('./mc_db_get1/mc_db_master.txt')

