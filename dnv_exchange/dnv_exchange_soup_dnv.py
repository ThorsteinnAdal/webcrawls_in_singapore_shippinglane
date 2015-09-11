__author__ = 'thorsteinn'

import urllib2
import re
from bs4 import BeautifulSoup
from db_format_helpers.is_number import is_number

def set_up(item_dict='summary'): # fields ['summary', 'dimensions', 'hullsummary', 'machinerysummary']
    """
    a setup call to adjust the various fields and names that exist on the dnv-exchange website in the different
    tabs.
    :param item_dict:
    :return: a dictionary the key in the dictionary becomes the name of the key in the final db
    the tuple that follows specifies the type of website field, the id of the field and finally what regex
    expression should be used to filter the returned value
    """
    if item_dict == 'summary':
        return {'dnv_id': ('span', 'ucMainControl_ToolContainer__ctl1_header_mDNVId', ''),
                'imo_id': ('span', 'ucMainControl_ToolContainer__ctl1_header_mIMONo', ''),
                'operation_status_s':('span', 'ucMainControl_ToolContainer__ctl1_header_mOperationalStatus', ''),
                'class_status_s':('span', 'ucMainControl_ToolContainer__ctl1_header_mClassStatus', ''),
                'ship_flag_s': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mFlag', ''),
                'callsign_s': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mSignalLetters', ''),
                'port_of_registry_s': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mPort', ''),
                'gt_n': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mGT', ''),
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


def main(requested_runs=40, wishlist_filename='wishlist.txt', **kwargs):
    """
    A script used for mining dnv-exchange for available ships using dnv-id
    Prior to using this script, a file containing a list of dnv-id's should be available.
    This "wishlist" can be generated by using json.dump() of a list into a file.

    Three items can be added as kwargs:
        1) a file name where collected records should be stored. This file could be 'dnv_get_1.txt'
        2) a file for log entries. This file will be overwritten each time.
        3) a file name for where db-collections should be stored
        4) a switch for verbose output
    :param requested_runs: how many records should be processed from the 'wishlist'. The default value is 40 (semi-fast)
    :param wishlist_filename: exact filename for the wishlist file.
    :param kwargs:  db_output_filename: the filename of the output file.
                    ids_completed_filename: The filename where the list of ids that are completed is stored.
                    log_filename:
    :return:
        1) The process picks up values from the wishlist_file and collects the records from dnv-exchange.
        2) The process formats the records in a dictionary formats and appends it to the file specified in 'db-output'
        3) The process removes the value from the wishlist_file
        4) The process is repeated 'rec' times'%s_processed.txt' % wishlist
    """
    from db_to_file_helpers.jsonDicts_to_file import append_db_to_file
    import json
    import os

    # Check if the wishlist points to an actual file
    if os.path.isfile(wishlist_filename) is False:
        print "%s does not exist. Make sure you have a valid file" % wishlist_filename
        return False
    else:
        # if the file exist, get the directory name
        work_directory = os.path.dirname(wishlist_filename)  # all other files should be saved in the same directory
        wishlist_file = os.path.basename(wishlist_filename)  # this is the actual file pointed to
        wishlist_n = os.path.splitext(wishlist_filename)[0]  # this is the first part of the file passed

        # get the list of id numbers that I need to work with
        with open(wishlist_filename, 'r') as f:
            dnv_wish_list = json.load(f)
            if len(dnv_wish_list) == 0:  # is the file empty? is the first item a number longer than 1
                print "%s is empty, provide a file that contains a list of dnv-ids" % wishlist_filename
                return False
            if len(dnv_wish_list[0]) > 1 and is_number(dnv_wish_list[0]) is False:
                print "check the format of the input file %s" % wishlist_filename
                return False

            # compare the number of runs requested and number of ids available
            if requested_runs > len(dnv_wish_list):
                requested_runs = len(dnv_wish_list)
            else:
                requested_runs = int(requested_runs)

        # take only the requested number of runs out of the wishlist
        part_list = dnv_wish_list[:requested_runs]

    # format names for other files that need to be generated.
    if 'db_output_filename' in kwargs.keys():
        name_grab = os.path.basename(kwargs.pop('db_output_filename'))  # this returns only the file name
        db_output_filename = os.path.join(work_directory, name_grab)
    else:
        db_output_filename = '%s_output.txt' % wishlist_n
    # this forces the log-file to be written into the same directory as the wishlist


    # do the same setup swap for the ids
    if os.path.isfile(db_output_filename) is False:
        open(db_output_filename, 'a').close()

    if 'ids_completed_filename' in kwargs.keys():
        name_grab = os.path.basename(kwargs.pop('ids_completed_filename'))
        ids_completed_filename = os.path.join(work_directory, name_grab)
    else:
        ids_completed_filename = '%s_completed.txt' % wishlist_n


    if os.path.isfile(ids_completed_filename) is False:
        open(db_output_filename, 'a').close()
        ids_collected = []
    else:
        try:
            with open(ids_completed_filename, 'r') as f:
                ids_collected = json.load(f)
        except Exception, me:
            print me.message

    if 'log_filename' in kwargs.keys():
        name_grab = os.path.basename(kwargs.pop('log_filename'))  # this returns only the file name
        log_filename = os.path.join(work_directory, name_grab)
    else:
        log_filename = '%s_log.txt' % wishlist_n


    verbose = kwargs.pop('verbose', True)

    if verbose:
        print '{message: <90}'.format(message="="*90)
        print '{message: <90}'.format(message=">  From dnv_exchange_soup_new.main:")
        print '{message: <90}'.format(message=">  File setup completed:")
        print '{message: <90}'.format(message=">  Wishlist of dnv-id values found in file: %s" % wishlist_file)
        print '{message: <90}'.format(message=">     All input and output records are printed to the root: %s" % work_directory)
        print '{message: <90}'.format(message=">     A list of completed dnv-ids is found in the file: %s" % os.path.basename(log_filename))
        print '{message: <90}'.format(message=">     db records are found in the file: %s" % os.path.basename(db_output_filename))
        print '{message: <90}'.format(message="="*90)

    # setup complete. Notify the start of process
    with open(log_filename, 'a') as f:
        f.write('='*20+'\nNew run:\n' + '='*20+'\n')
        message = "Currently there are %s records for ships and %s records left" %\
                  (len(ids_collected), len(dnv_wish_list))
        f.write(message + '\nCurrent request:\n')
        json.dump(part_list, f)
        f.write('\n')
        if verbose:
             print message

    # HERE BE DRAGONS = here the process starts
    cycle_count = 1
    for dnv_id in part_list[:]:
        with open(log_filename, 'a') as f:
            message = "%s of %s : Processing dnv_id = %s" % \
                      (cycle_count, requested_runs, str(dnv_id))
            f.write(message + '; ')
            if verbose:
                print message

        # create a name and an empty db for the data
        entry_name = 'dnv%s' % str(dnv_id)
        db = {}
        db[entry_name] = dnv_soup_master(dnv_id)    # this process gets the data from the website
        append_db_to_file(db, db_output_filename)   # this function adds the collected db to the appointed file

        ids_collected.append(dnv_id)                # this adds the id number to the "collected ids list
        dnv_wish_list.remove(dnv_id)                # this removes the id from the wishlist list
        part_list.remove(dnv_id)                    # this removes the id from the part-list (for debugging reason)

        # log the process
        with open(log_filename, 'a') as f:
            f.write(message)
            f.write('\n'+'-'*20+'\nRemaining list: \n')
            json.dump(part_list, f)
            f.write('\n')
            if verbose:
                message = "Obtained db with length = %s items" % len(db[entry_name])
                print message

        # dump the process into the correct files
        with open(ids_completed_filename, 'w') as f:
            json.dump(ids_collected, f)
        with open(wishlist_filename, 'w') as f:
            json.dump(dnv_wish_list, f)

        cycle_count += 1

    print "From dnv_exchange_soup_new.main.\n " \
          "Process completed: \nOutput file: %s.\nLogfile: %s" % \
          (db_output_filename, db_output_filename)


# main(requested_runs=4200,
#     wishlist_filename='./dnv_exchange_get2/dnv_wishlist.txt',
#     db_output_filename='dnv_wishlist_output_4.txt',
#     log_filename='dnv_wishlist_log_4.txt')


def dnv_unify_get_documents(folder, file_base):
    from glob import glob
    import os
    from db_to_file_helpers.jsonDicts_to_file import file_to_db, db_to_file

    foot = os.path.dirname(folder)
    ff=os.path.join(foot, file_base)
    file_glob = glob(ff + '*')


    db = {}
    for one_file in file_glob:
        print one_file
        smalldb = file_to_db(one_file)
        db.update(smalldb)

    db_to_file(db, os.path.join(foot, 'dnv_db_master.txt'))
    print "Collcted {number} of records into the output file: {output_file}".format(number=len(db), output_file=os.path.join(foot, 'dnv_db_master.txt'))

#dnv_unify_get_documents('./dnv_exchange_get2/', 'dnv_wishlist_output')


if __name__ == '__main__':
    main(requested_runs=3200,
         wishlist_filename='./dnv_exchange_get2/dnv_wishlist.txt',
         db_output_filename='dnv_wishlist_output_7.txt',
         log_filename='dnv_wishlist_log_7.txt')

