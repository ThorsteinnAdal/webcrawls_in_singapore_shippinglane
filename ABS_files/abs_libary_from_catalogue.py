__author__ = 'thorsteinn'

import csv
import json
from db_to_file_helpers.jsonDicts_to_file import db_to_file
from db_format_helpers.ship_fields import rename_ship_field, stringnumbers_to_numbers, list_all_field_values

# ABS catalogue is a csv file that I copied from the abs website. The catalogue has all the publicly available ships and their abs_id
# I intend to get those ship infos from online by using delicious soup

# first open the file and convert the file into a format that I like to work with
with open('./data_files/ABS_catalogue', 'r') as f:
    csvfile = csv.DictReader(f)
    fields = csvfile.fieldnames
    db = {}
    print fields
    for line in csvfile:
        itm = 'abs%s' % line['Class Number']
        db[itm] = line

    rename_ship_field('Class Number', 'abs_id', db)
    rename_ship_field('IMO Number', 'imo_id', db)
    rename_ship_field('Name', 'name_s', db)
    rename_ship_field('Type', 'abs_gen_type_s', db)

# then collect all the abs_id values
    abs_id_values = list_all_field_values('abs_id', db)

# output the dictionary to a database
    db_to_file(db, './data_files/abs_catalogue.txt')

# output the list of ids to a file
    with open('./data_files/abs_ids.txt', 'w') as f:
        json.dump(abs_id_values, f)

# each ship info should be available to me through the website:
# https://www.eagle.org/safenet/record/record_vesseldetailsprinparticular?Classno=7706205&Accesstype=PUBLIC
# https://www.eagle.org/safenet/record/record_vesseldetailshull?Classno=6001177&Accesstype=PUBLIC
# https://www.eagle.org/safenet/record/record_vesseldetailscapacity?Classno=6001177&Accesstype=PUBLIC
# https://www.eagle.org/safenet/record/record_vesseldetailsmach?Classno=6001177&Accesstype=PUBLIC
# https://www.eagle.org/safenet/record/record_vesseldetailsliftequipment?Classno=6001177&Accesstype=PUBLIC
# https://www.eagle.org/safenet/record/record_ownerManager?Classno=6001177&Accesstype=PUBLIC

