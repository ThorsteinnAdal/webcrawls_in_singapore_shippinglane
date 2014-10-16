__author__ = 'thorsteinn'

import json
from db_to_file_helpers.jsonDicts_to_file import file_to_db

# first pick up the db from the maritime connection
db = file_to_db('../output_files/mc_db_get_1_fixed.txt')

# find the ships in that db which are in DNV, or Germanische Lloyds
ships = db.keys()

classification_societies = ['DET NORSKE VERITAS', 'GERMANISCHER LLOYD']

mc_ships_in_dnv = []
for ship in ships:
    ship_db = db[ship]
    class_society = 'Class society'
    if 'Class society' in ship_db.keys():
        if ship_db[class_society] == 'DET NORSKE VERITAS':
            mc_ships_in_dnv.append(ship_db['imo_id'])
        else:
            if ship_db[class_society] not in classification_societies:
                classification_societies.append(ship_db[class_society])


# ships_in_dnv now contains the imo numbers for all ships that were found to have either DNV or GL as a classification society
# other societies found are stored in otherSocieties. Output this list into a file

with open('../output_files/mc_db_get_1_shipClassification_societies.txt','w') as f:
    json.dump(classification_societies, f)

# now find the imos that I have collected from dnv_db_get_1
with open('../output_files/dnv_db_get_1_imosCollected.txt', 'r') as f:
    dnv_imos_found = json.load(f)

# throw ships already found in dnv database out of the list of ships with DNV or GL class society in the mc
for imo in mc_ships_in_dnv[:]:
    if imo in dnv_imos_found:
        mc_ships_in_dnv.remove(imo)

# save this list to a file for later use
with open('../output_files/dnv_db_get_1_imosToCheck.txt', 'w') as f:
    json.dump(mc_ships_in_dnv, f)

print 'Found: %s new imo numbers' % len(mc_ships_in_dnv)