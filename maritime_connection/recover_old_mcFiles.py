__author__ = 'thorsteinn'

import os
import re
from db_to_file_helpers.jsonDicts_to_file import file_to_db, db_to_file

file_list = os.listdir('input_files/')

for fileName in file_list[:]:
    if len(re.findall(r'.json', fileName)) is 0:
        file_list.remove(fileName)

db = {}
for fileName in file_list:
    oneFile = './input_files/%s' % fileName
    print oneFile
    db.update(file_to_db('input_files/%s' % fileName))

db_to_file(db, '../output_files/mc_db_get_1.txt')

