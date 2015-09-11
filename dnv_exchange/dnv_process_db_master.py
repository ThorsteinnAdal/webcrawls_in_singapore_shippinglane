__author__ = 'thorsteinn'

from db_to_file_helpers.jsonDicts_to_file import file_to_db, db_to_file
from db_format_helpers.strings_in_fields_to_numbers import strings_in_fields_to_numbers
import os
from db_format_helpers.set_blanks_to_None import set_blanks_to_None


def dnv_process_1(db_input_file, **kwargs):

###### setup segment
    if os.path.isfile(db_input_file) is False:
        print "Select an existing db file"
        return False
    else:
        work_folder = os.path.dirname(db_input_file)
        input_file_n = os.path.splitext(db_input_file)[0]
    try:
        db = file_to_db(db_input_file)
    except Exception, me:
        print me.message
        return False

    if 'output_file' in kwargs.keys():
        output_file = kwargs.pop('output_file')
    else:
        output_file = os.path.join(work_folder, input_file_n + '_fix.txt')

###### end of setup segment

    print "setting input to {input_file}, setting output to {output_file}".format(input_file=db_input_file, output_file=output_file)

###### processing data-fields
    strings_in_fields_to_numbers(None, db)
    set_blanks_to_None('all', db, trailing_blanks=True)

    db_to_file(db, output_file)


if __name__ == '__main__':
    dnv_process_1('./dnv_exchange_get2/dnv_db_master.txt', output_file='./dnv_exchange_get2/dnv_db_master_fix.txt')
