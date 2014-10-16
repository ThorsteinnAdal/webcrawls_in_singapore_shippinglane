__author__ = 'thorsteinn'

import urllib2
import re
from bs4 import BeautifulSoup

def set_up(item_dict='summary'): # fields ['summary', 'dimensions', 'hullsummary', 'machinerysummary']
    if item_dict == 'summary':
        return {'dnv_id': ('span', 'ucMainControl_ToolContainer__ctl1_header_mDNVId', ''),
                'ship_flag_s': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mFlag', ''),
                'callsign_s': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mSignalLetters', ''),
                'port_of_registry_s': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mPort', ''),
                'gwt_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mGT', ''),
                'owner_dnv_id': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mOwnerNumber', r'\d+'),
                'owner_imo_id': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mOwnerLRF', r'\d+'),
                'nt_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mNT', ''),
                'dwt_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mDWT', ''),
                'manager_dnv_id': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mManagerNumber', r'\d+'),
                'manager_imo_id': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mManagerLRF', r'\d+'),
                'yard_dnv_id': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mYardNo', ''),
                'build_year_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mBuilt', ''),
                'dnv_type_text': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mType', ''),
                'dnv_class_text': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mClass', ''),
                'capacity_text': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mRegister', ''),
                'owner_s': ('a', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mOwner', ''),
                'manager_s': ('a', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mManager', ''),
                'yard_s': ('a', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mYard', '')
                 }
    elif item_dict =='dimensions':
        return {'length_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Loa', r'[-+]?\d+.?\d+'),
                   'length_between_perpendiculars_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Lbp', r'[-+]?\d+.?\d+'),
                   'length_load_label_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Lload', r'[-+]?\d+.?\d+'),
                   'length_of_water_line_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Lwl', r'[-+]?\d+.?\d+'),
                   'width_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Bext', r'[-+]?\d*.?\d+'),
                   'depth_mulded_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_D', r'[-+]?\d*.?\d+'),
                   'draught_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Draught', r'[-+]?\d*.?\d+'),
                   'freeboard_note_text': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Freeboard', '')
                   }
    elif item_dict == 'hullsummary':
        return  {'cranes_text': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_CraneCapacity', ''),
                   'hull_superstructure_text': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Superstructures', ''),
                   'hull_trans_bulkheads_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_TransBulkheads', ''),
                   'hull_decks_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Decks', ''),
                   'hull_long_bulkheads_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_LongBulkheads', ''),
                   'hull_other_openings_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_OtherOpenings', ''),
                   'hull_cargo_tanks_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_CargoTanks', ''),
                   'hull_side_openings_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_SideOpenings', ''),
                   'cargo_max_grain_s': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Grain', ''),
                   'cargo_max_bale_s': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Bale', ''),
                   'cargo_max_liquid_s': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Liquid', ''),
                   'cargo_pumps_s': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Pumps', ''),
                   'cargo_pump_capacity_s': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_PumpCapacity', ''),
                   'cargo_pump_rooms_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_PumpRooms', ''),
                   'hatchway_dim_s': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_HatchwayDim', ''),
                   'ballast_capacity_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_BallastCapacity', r'[-+]?\d*.?\d+'),
                   }
    elif item_dict == 'machinerysummary':
        return ['ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mGrid', '']
    else:
        return False


def dnv_exchange_soup(dnv_id, sub_view='summary', item_dict=set_up('summary')):
    url = 'https://exchange.dnv.com/exchange/main.aspx?extool=vessel&subview=%s&vesselid=%s' % (sub_view, dnv_id)
    db = {'dnv_id': dnv_id}

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    try:
        page = opener.open(url)
        soup = BeautifulSoup(page.read())
    except Exception, e:
        db[sub_view] = 'error'
        print e.message
        return db


    # check if a correct page has been found
    page_title=soup.title.text
    ship_name = re.findall('[A-Z][A-Z]+', page_title)[1:]
    if len(ship_name):
        db['name_s'] = ' '.join(ship_name)
    else:
        db['name_s'] = None
        return db

    if type(item_dict) is dict:
        items_to_find = item_dict
    else:
        items_to_find = set_up(item_dict)

    # Loop through the items to find library
    for key in items_to_find:
        thing_found = soup.find(items_to_find[key][0], id=items_to_find[key][1])
        if len(thing_found.contents) != 0:
            if len(items_to_find[key][2]):
                match = re.findall(items_to_find[key][2], thing_found.text)
                db[key] = match[0]
            else:
                db[key] = thing_found.text

    return db



def dnv_exchange_soup_machine_table(dnv_id, sub_view='machinerysummary', item_dict='machinerysummary'):

    url = 'https://exchange.dnv.com/exchange/main.aspx?extool=vessel&subview=%s&vesselid=%s' % (sub_view, dnv_id)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    try:
        page = opener.open(url)
        soup = BeautifulSoup(page.read())
    except Exception, e:
        print e.message
    if type(item_dict) is dict:
        items_to_find = item_dict
    elif type(item_dict) is list:
        items_to_find = item_dict
    else:
        items_to_find = set_up(item_dict)

    # check if the IMO number returns a ship title, if it doesn't return a blank name
    theTitle=soup.title.text
    shipAndPage = re.findall(r'\w+', theTitle)[2:-1]
    if shipAndPage.__contains__('Machinery'):
        theTable=soup.find('table', id=items_to_find[0])
        tableRows=theTable.find_all('tr')

        linePack=[]
        for row in tableRows:
            oneRow=row.find_all('td')
            oneLine=[]
            for cell in oneRow:
                toAppend = cell.text
                toAppend = ' '.join(toAppend.split())
                if 'NOT SET' == toAppend:
                    toAppend=''
                oneLine.append(toAppend)
            linePack.append(oneLine)

        return linePack


def dnv_soup_master(dnv_id):
    db = {}
    summary_info = dnv_exchange_soup(dnv_id, 'summary', set_up('summary'))
    db.update(summary_info)

    if summary_info['name_s'] is not None:
        dimensions = dnv_exchange_soup(dnv_id, 'dimensions', set_up('dimensions'))
        db.update(dimensions)

        hull_info = dnv_exchange_soup(dnv_id, 'hullsummary', set_up('hullsummary'))
        db.update(hull_info)

        machin_info = {'machinery_l': dnv_exchange_soup_machine_table(dnv_id, 'machinerysummary', set_up('machinerysummary'))}
        db.update(machin_info)
    return db


def main(requested_runs=40, wishlist_filename='./dnv_exchange_gets/dnv_ids_to_get.txt', **kwargs):
    """
    A script used for mining dnv-exchange for available ships using dnv-id
    Prior to using this script, two files should be available:
        1) a file containing a list of ship records that have been obtained. This file could be 'dnv_ids_obtained.txt'
        2) a file containing a list of ship records that you want to obtain. This file could be 'dnv_ids_to_get.txt'
            THIS FILE SHOULD NOT BE EMPTY
    two more files should be specified:
        1) a file name where collected records should be stored. This file could be 'dnv_get_1.txt'
        2) a file for log entries. This file will be overwritten each time.
    the file paths should be exact, otherwise the /. folder will be used
    :param requested_runs: how many records should be processed from the 'wishlist'. The default value is 40 (semi-fast)
    :param wishlist_filename: exact filename for the wishlist file. default value is './dnv_exchange_gets/dnv_ids_to_get.txt'
    :param kwargs: setup for optional outputs:
        {db_output: the filename of the output file. Default value is './dnv_exchange_gets/dnv_db_get_11.txt'
         ids_completed: The filename where the list of ids that are completed is stored. The default is './dnv_exchange_gets/dnv_ids_obtained.txt'
         log_file: The log. The default is './dnv_exchange_gets/dnv_db_get_n_log.txt'
    :return:
        1) The process picks up values from the wishlist_file and collects the records from dnv-exchange.
        2) The process formats the records in a dictionary formats and appends it to the file specified in 'db-output'
        3) The process removes the value from the wishlist_file
        4) The process is repeated 'rec' times
    """
    from db_to_file_helpers.jsonDicts_to_file import append_db_to_file
    import json
    import os

    here = os.path.abspath(os.path.dirname(__file__))
    print here

    db_output_filename = kwargs.pop('db_output_filename', './dnv_exchange_gets/dnv_db_get_11.txt')
    ids_completed_filename = kwargs.pop('ids_completed_filename', './dnv_exchange_gets/dnv_ids_obtained.txt')
    log_filename = kwargs.pop('log_filename', './dnv_exchange_gets/dnv_db_get_n_log.txt')


    with open(ids_completed_filename, 'r') as f:
        ids_collected = json.load(f)

    with open(wishlist_filename, 'r') as f:
        dnv_wish_list = json.load(f)
        if requested_runs > len(dnv_wish_list):
            requested_runs = len(dnv_wish_list)
        elif len(dnv_wish_list) == 0:
            print 'The file %s is empty' % dnv_wish_list
        else:
            requested_runs = int(requested_runs)

    part_list = dnv_wish_list[:requested_runs]

    print "From dnv_exchange_soup_new.main:\nProcess started"
    number_of_requests = len(part_list[:])

    with open(log_filename, 'a') as f:
        f.write('='*20+'\nNew run:\n' + '='*20+'\n')
        message = "Currently there are %s records for ships and %s records left" % (len(ids_collected), len(dnv_wish_list))
        print message
        f.write(message + '\nCurrent request:\n')
        json.dump(part_list, f)
        f.write('\n')

    cycle_count = 1
    for dnv_id in part_list[:]:
        with open(log_filename, 'a') as f:
            message = "%s of %s : Processing dnv_id = %s" % (cycle_count, number_of_requests, str(dnv_id))
            print message
            f.write(message + '; ')

        entry_name = 'dnv%s' % str(dnv_id)
        db = {}
        db[entry_name] = dnv_soup_master(dnv_id)
        append_db_to_file(db, db_output_filename)

        ids_collected.append(dnv_id)
        dnv_wish_list.remove(dnv_id)

        part_list.remove(dnv_id)

        with open(log_filename, 'a') as f:
            message = "Obtained db with length = %s items" % len(db[entry_name])
            print "Obtained db with length = %s items" % len(db[entry_name])
            f.write(message)
            f.write('\n'+'-'*20+'\nRemaining list: \n')
            json.dump(part_list, f)
            f.write('\n')
        with open(ids_completed_filename, 'w') as f:
            json.dump(ids_collected, f)
        with open(wishlist_filename, 'w') as f:
            json.dump(dnv_wish_list, f)

        cycle_count += 1

    print "From dnv_exchange_soup_new.main.\n " \
          "Process completed: \nOutput file: %s.\nLogfile: %s" % (db_output_filename, db_output_filename)
    if len(part_list):
        print "%s items remain of %s items initially requested." \
              " Unprocessed items are in file: %s." % (len(part_list), number_of_requests, log_filename)


main(requested_runs=400,
     wishlist_filename='./dnv_exchange_gets/dnv_ids_to_get.txt',
     ids_completed_filename='./dnv_exchange_gets/dnv_ids_obtained.txt',
     log_filename='./dnv_exchange_gets/dnv_db_get_10_log.txt',
     db_output_filename='./dnv_exchange_gets/dnv_db_get_10.txt')


def dnv_unify_get_documents():
    from db_to_file_helpers.jsonDicts_to_file import file_to_db, db_to_file
    my_root = './dnv_exchange_gets/'
    file_list = [my_root + 'dnv_db_get_1.txt',
                my_root + 'dnv_db_get_2.txt',
                my_root + 'dnv_db_get_3.txt',
                my_root + 'dnv_db_get_4.txt',
                my_root + 'dnv_db_get_11.txt',
                my_root + 'dnv_db_get_6.txt',
                my_root + 'dnv_db_get_5.txt',
                my_root + 'dnv_db_get_7.txt',
                my_root + 'dnv_db_get_8.txt',
                my_root + 'dnv_db_get_9.txt',
                my_root + 'dnv_db_get_10.txt']
    db = {}
    for one_file in file_list:
        print one_file
        smalldb = file_to_db(one_file)
        db.update(smalldb)

    db_to_file(db, my_root+'dnv_db_master.txt')

# dnv_unify_get_documents()

if __name__ == '__main__':
    pass