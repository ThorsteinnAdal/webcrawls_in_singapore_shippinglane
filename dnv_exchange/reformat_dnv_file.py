__author__ = 'thorsteinn'

from db_to_file_helpers.jsonDicts_to_file import file_to_db, db_to_file
from db_format_helpers.ship_fields import get_all_ship_fields, rename_ship_field, stringnumbers_to_numbers, \
    drop_ships_by_key_value, list_all_field_values
import json

db = file_to_db('../output_files/dnv_db_get_1.txt')

rename_ship_field('IMO id', 'imo_id', db)
rename_ship_field('Ship name', 'name_s', db)
rename_ship_field('Owner LRF id', 'owner_id', db)
rename_ship_field('Draught', 'draught_n', db)
rename_ship_field('Construction Yard id', 'yard_id', db)
rename_ship_field('Ballast capacity in m3', 'ballast_capacity_f', db)
rename_ship_field('Owner id', 'owner_id', db)
rename_ship_field('Width extreme in m', 'width_extreme_n', db)
rename_ship_field('Year built', 'year_d', db)
rename_ship_field('Freeboard note', 'freeboard_note_s', db)
rename_ship_field('Manager LRF id', 'manager_id', db)
rename_ship_field('Ship Owner', 'owner_s', db)
rename_ship_field('Length load label in m', 'length_load_label_n', db)
rename_ship_field('Manager id', 'manager_id', db)
rename_ship_field('Machinery', 'machinery_l', db)
rename_ship_field('GWT', 'gt_n', db)
rename_ship_field('Depth mulded in m', 'depth_mulded_n', db)
rename_ship_field('Net Tonnage', 'net_tonnage_n', db)
rename_ship_field('DNV id', 'dnv_id', db)
rename_ship_field('Draugth', 'draught_n', db)
rename_ship_field('Capacity', 'capacity_s', db)
rename_ship_field('DWT', 'dwt_n', db)
rename_ship_field('GTW', 'gt_n', db)
rename_ship_field('DNV Class', 'dnv_class_s', db)
rename_ship_field('Length in m', 'length_n', db)
rename_ship_field('Construction yard', 'yard_s', db)
rename_ship_field('Manager', 'manager_s', db)
rename_ship_field('Callsign', 'callsign_s', db)
rename_ship_field('Port of Registry', 'port_reg_s', db)
rename_ship_field('Ship flag', 'flag_s', db)
rename_ship_field('Crane capacity', 'crane_info_s', db)
rename_ship_field('Hull trans bulkheads', 'hull_trams_bulkheads_n', db)
rename_ship_field('Cargo pumps', 'cargo_pumps_n', db)
rename_ship_field('Cargo pump rooms', 'cargo_pump_rooms_n', db)
rename_ship_field('Hull cargo tanks', 'hull_cargo_tanks', db)
rename_ship_field('Hull decks', 'hull_decks_s', db)
rename_ship_field('Hull long bulkheads', 'hull_bulkheads_s', db)
rename_ship_field('Hatchway dimensions', 'hatchway_dim_s', db)
rename_ship_field('DNV Type', 'dnv_type_s', db)

print get_all_ship_fields(db)

stringnumbers_to_numbers(db)

imosChecked = list_all_field_values('imo_id', db)
with open('../output_files/dnv_db_get_1_imosChecked.txt', 'w') as f:
    json.dump(imosChecked, f)

db_to_file(db,'temp.txt')

drop_ships_by_key_value('name_s', None, db)

imosCollected = list_all_field_values('imo_id', db)
with open('../output_files/dnv_db_get_1_imosCollected.txt', 'w') as f:
    json.dump(imosCollected, f)
db_to_file(db,'../output_files/dnv_db_get_1_fixed.txt')
