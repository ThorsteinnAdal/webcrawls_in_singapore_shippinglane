__author__ = 'thorsteinn'

from db_to_file_helpers.jsonDicts_to_file import file_to_db, db_to_file
from db_format_helpers.ship_fields import get_all_ship_fields, rename_ship_field, stringnumbers_to_numbers, \
    drop_ships_by_key_value, list_all_field_values
import json


def main(db_input_file, db_output_file):
    db = file_to_db(db_input_file)

    rename_ship_field('ballast_capacity_n', 'ballast_capacity_f', db)
    stringnumbers_to_numbers('ballast_capacity_f', db)
    rename_ship_field('capacity_text', 'capacity_s', db)
    rename_ship_field('cargo_pumps_s', 'cargo_pumps_n', db)
    rename_ship_field('cranes_text', 'crane_info_s', db)
    rename_ship_field('width_extreme_n', 'width_n', db)
    stringnumbers_to_numbers('width_n', db)
    rename_ship_field('hull_cargo_tanks', 'hull_cargo_tanks_s', db)
    rename_ship_field('hull_cargo_tanks_n', 'hull_cargo_tanks_s', db)
    stringnumbers_to_numbers('hull_cargo_tanks_n', db)
    rename_ship_field('Hull superstructure', 'hull_superstructure_s', db)
    rename_ship_field('hull_superstructure_text', 'hull_superstructure_s', db)
    rename_ship_field('Length between perpendiculars in m', 'length_between_perpendiculars_n', db)
    stringnumbers_to_numbers('length_between_perpendiculars_n', db)
    stringnumbers_to_numbers('depth_mulded_n', db)
    rename_ship_field('dnv_class_text', 'dnv_class_s', db)
    rename_ship_field('yard_id', 'yard_dnv_id', db)
    stringnumbers_to_numbers('yard_dnv_id', db)
    rename_ship_field('owner_id', 'owner_imo_id', db)
    rename_ship_field('dnv_type_text', 'dnv_type_s', db)
    rename_ship_field('freeboard_note_text', 'freeboard_note_s', db)
    rename_ship_field('manager_id', 'manager_imo_id', db)
    rename_ship_field('net_tonnage_n', 'nt_n', db)
    stringnumbers_to_numbers('nt_n', db)
    rename_ship_field('gwt_n', 'gt_n', db)
    stringnumbers_to_numbers('gt_n', db)
    rename_ship_field('hull_trams_bulkheads_n', 'hull_trans_bulkheads_n', db)
    stringnumbers_to_numbers('hull_trans_bulkheads_n', db)
    stringnumbers_to_numbers('hull_long_bulkheads_n', db)
    stringnumbers_to_numbers('dnv_id', db)
    stringnumbers_to_numbers('draught_n', db)
    stringnumbers_to_numbers('length_load_label_n', db)

    db_to_file(db, db_output_file)


if __name__ == '__main__':
    main('./dnv_exchange_gets/dnv_db_master.txt', './dnv_exchange_gets/dnv_db_fixed.txt')