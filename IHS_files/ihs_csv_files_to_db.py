__author__ = 'thorsteinn'
import unicodecsv
import json

def csv_to_db(file_name):
    with open(file_name, 'r') as f:
        csvReader = unicodecsv.DictReader(f)
        print csvReader.fieldnames


csv_to_db('./ihs_data/ShipData.CSV')