__author__ = 'thorsteinn'

from db_to_file_helpers.jsonDicts_to_file import file_to_db, db_to_file
from db_format_helpers.ship_fields import rename_ship_field, stringnumbers_to_numbers, drop_ships_by_key_value, list_all_field_values
import json

db = file_to_db('../output_files/mc_db_get_1.txt')

rename_ship_field('Name of the ship', 'name_s', db)
rename_ship_field('MMSI', 'mmsi_id', db)
rename_ship_field('IMO number', 'imo_id', db)
rename_ship_field('Flag', 'flag_s', db)
rename_ship_field('Name of ship', 'name_s', db)
rename_ship_field('DWT', 'dwt_n', db)
rename_ship_field('Former names', 'former_names_l', db)
rename_ship_field('Last known flag', 'last_flags_l', db)
rename_ship_field('Gross tonnage', 'gt_n', db)
rename_ship_field('Year of build', 'year_d', db)
rename_ship_field('Manager & owner', 'manager_owner_s', db)
rename_ship_field('Manager', 'manager_s', db)
rename_ship_field('Owner', 'owner_s', db)
rename_ship_field('Type of ship', 'ship_type_s', db)
rename_ship_field('Home port', 'flag_port_s', db)

stringnumbers_to_numbers(db)

imoNumbers_checked = sorted(list_all_field_values('imo_id', db))
with open('../output_files/mc_db_get_1_imosChecked.txt', 'w') as f:
    json.dump(imoNumbers_checked, f )

drop_ships_by_key_value('name_s', None, db)

imoNumbers_completed = sorted(list_all_field_values('imo_id', db))
with open('../output_files/mc_db_get_1_imosCollected.txt', 'w') as f:
    json.dump(imoNumbers_completed, f )

db_to_file(db, '../output_files/mc_db_get_1_fixed.txt')
