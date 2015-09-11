__author__ = 'thorsteinn'

from dnv_exchange.input_files.dbDNV1 import db as db1
from dnv_exchange.input_files.dbDNV2 import db as db2
from dnv_exchange.input_files.dbDNV3 import db as db3
from dnv_exchange.input_files.dbDNV4 import db as db4
from dnv_exchange.input_files.dbDNV5 import db as db5
from dnv_exchange.input_files.dbDNV6 import db as db6
from dnv_exchange.input_files.dbDNV7 import db as db7
from dnv_exchange.input_files.dbDNV8 import db as db8
from dnv_exchange.input_files.eimskipaskip_DNV import db as db9

from db_to_file_helpers.jsonDicts_to_file import db_to_file


db = {}
db.update(db1)
db.update(db2)
db.update(db3)
db.update(db4)
db.update(db5)
db.update(db6)
db.update(db7)
db.update(db8)
db.update(db9)

db_to_file(db, '../output_files/dnv_db_get_1.txt')
