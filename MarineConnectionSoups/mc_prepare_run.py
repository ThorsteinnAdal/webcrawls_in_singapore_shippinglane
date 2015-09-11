__author__ = 'thorsteinn'
from db_to_file_helpers.jsonDicts_to_file import file_to_db
from db_format_helpers.list_all_field_values import list_all_field_values
import json
import os

def new_imo_list(wishlist, old_db_file, newer_db_file):

    db_files = [old_db_file, newer_db_file]

    imo_list = []
    for file in db_files:
        if os.path.isfile(file):
            print "The input file: {file_name} was {conclusion}".format(
                file_name=file,
                conclusion='found.'
            )
        else:
            print "The input file: {file_name} was {conclusion}".format(
                file_name=file,
                conclustion='not found, correct the address and try again.'
            )
            return False


        try:
            db = file_to_db(file)
            imo_list.append(list_all_field_values('imo_id', db))
        except Exception, me:
            print me.message
            return False

    old_imo_list = imo_list[0]
    new_imo_list = imo_list[1]
    for imo in old_imo_list:
        if imo in new_imo_list:
            new_imo_list.remove(imo)

    if wishlist:
        try:
            with open(wishlist, 'w') as f:
                json.dump(new_imo_list, f)
            print "A list of {imoLength} numbers was generated and exported to the file {file}".format(
                imoLength=len(new_imo_list),
                file=wishlist
            )
        except Exception, me:
            print me.message
            return False
    else:
        return new_imo_list

new_imo_list('./mc_get2/wishlist.txt',
                    './mc_db_get1/mc_db_master_fix_1.txt',
                    '../dnv_exchange/dnv_exchange_get2/dnv_db_master_fix.txt')


