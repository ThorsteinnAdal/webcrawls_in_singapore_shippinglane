__author__ = 'TA'

import urllib2
from bs4 import BeautifulSoup
from db_to_file_helpers.jsonDicts_to_file import db_to_file, file_to_db
from db_format_helpers.ship_fields import get_all_ship_fields, list_all_field_values
import unicodecsv
import json

def dnv_registry_listing_soup(alphabetLetter, output_file_base):
    """
    A method for collecting the list of ships that are in the DNV registry. From this list a list of available dnv-ids can be generated.
    :param alphabetLetter: A capital letter of the alphabet
    :param output_file_base: The base_name of the output file
    :return: Creates a file with db from the collection
    """
    url = 'https://exchange.dnv.com/exchange/Main.aspx?extool=VReg&Search=%s' % alphabetLetter
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    # open the page
    try:
        page = opener.open(url)
        soup = BeautifulSoup(page.read())
    except Exception, m:
        print m.message


    # try to read the header
    try:
        validPage = soup.find('title').contents[0]
        if 'Exchange' not in validPage.split():
            return 'page not found'
    except Exception as m:
        print m.message


    # pick up the table
    dataTable = soup.find('table', id='ucMainControl_ToolContainer__ctl1_selectVesselOutputControl_mGrid')
    dataRows = dataTable.find_all('tr', attrs={'class':'Data'})

    db = {}
    j = 0
    for row in dataRows:
        row_tag = alphabetLetter+str(j)
        db[row_tag] = {
            'status_s': row.contents[1].text.strip() if row.contents[1].text.strip() else None,
            'name_s': row.contents[2].text.strip() if row.contents[2].text.strip() else None,
            'dnv_id': row.contents[3].text.strip() if row.contents[3].text.strip() else None,
            'dnv_type_s': row.contents[4].text.strip() if row.contents[2].text.strip() else None,
            'build_year_n': row.contents[5].text.strip() if row.contents[5].text.strip() else None,
            'builder_s': row.contents[6].text.strip() if row.contents[6].text.strip() else None
        }
        j+=1

    if output_file_base:
        file_name = output_file_base + '_' + alphabetLetter + '.txt'
        db_to_file(db, file_name)

    print 'Completed collection of %s-letter ships from DNV exchange db' % alphabetLetter

def dnv_collect_registry_listing(base_name):
    """
    a method that cycles through the alphabet and collects one page per alphabet
    :param base_name: the base name of the output file
    :return: a single filename
    """
    theLetters = map(chr, range(65, 91))
    for aLetter in theLetters:
        print "Requesting file for the letter: %s" % aLetter
        dnv_registry_listing_soup(aLetter, base_name)

def dnv_unify_registryListing(output_file, db_file_base_name, csvSwitch=0):
    """
    A script that unifies all db-txt files to a single file and returns one file
    :param output_file: the name of the output file
    :param csvSwitch: a switch to pick if a csv file is to be generated
    :return: a single file
    """
    db={}
    theLetters = map(chr, range(65, 91))
    for letter in theLetters:
        file_name = db_file_base_name + '_' + letter + 'txt'
        db.update(file_to_db(file_name))
    if csvSwitch:
        file_name = output_file + ".csv"
        with open(file_name, 'w') as f:
            fields = get_all_ship_fields(db)
            csvWriter = unicodecsv.DictWriter(f, fields, encoding='utf-8')
            ships = db.keys()
            csvWriter.writeheader()
            for ship in ships:
                csvWriter.writerow(db[ship])
    else:
        db_to_file(db, output_file+'.txt')

#dnv_unify_registryListing('dnv_directory_list2.csv',1)


'''
several processing functions to extract values from the listing once they have been generated.

'''

def dnv_generate_wishlist(dnv_listing_db_file, wishlist_file_name):
    """
    A method for creating a simple file with all dnv-ids that are in a specific dnv_listing_db_file
    :param dnv_listing_db_file: the exact name of the start-file
    :return: returns a json file with the list
    """
    print "Extracting dnv-id values from %s" % dnv_listing_db_file
    db = file_to_db(dnv_listing_db_file)
    if 'dnv_id' in get_all_ship_fields(db):
        list = list_all_field_values('dnv_id', db)
        with open(wishlist_file_name, 'w') as f:
            json.dump(list, f)

        print "Found %s ids, dumped them into the file.\nKTHXBYE" % len(list)
    else:
        print "dnv-id field not found in the file"

dnv_generate_wishlist('./dnv_registry_output/dnv_listing.txt', './dnv_exchange_get2/dnv_wishlist.txt')


'''
----------------- MAIN ----------
'''

def main(base_name = 'dnv_listing'):
    print "Starting process for files named %s" % base_name
    dnv_collect_registry_listing(base_name)
    print "Collection of listing completed. Unifying lists"
    dnv_unify_registryListing('dnv_directory_list', base_name, 1)
    print "Process completed"


if __name__ == '__main__':
    pass