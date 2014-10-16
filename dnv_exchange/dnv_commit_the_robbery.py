__author__ = 'thorsteinn'

from dnv_exchange.dnv_exchange_soup import buildMasterTable
import json
from db_to_file_helpers.jsonDicts_to_file import append_db_to_file


# '../output_files/dnv_db_get_1_imosToCheck.txt'
with open('not_done.txt', 'r') as f:
    imo_list = json.load(f)

oneIMO = 9086801
db = {}
work_list = imo_list[:]
run_number = 1
for imo in imo_list:
    print 'started attack: %s on imo = %s' % (run_number, str(imo))
    db['imo%s' % str(imo)] = buildMasterTable(imo)
    print 'completed attack'
    append_db_to_file(db, 'someShips.txt')
    work_list.remove(imo)
    with open('not_done.txt', 'w') as f:
        json.dump(work_list, f)
    run_number += 1
    db = {}

