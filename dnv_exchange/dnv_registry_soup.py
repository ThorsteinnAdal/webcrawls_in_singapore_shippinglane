__author__ = 'TA'

import urllib2
from bs4 import BeautifulSoup
from db_to_file_helpers.jsonDicts_to_file import db_to_file, file_to_db
from db_format_helpers.ship_fields import get_all_ship_fields
import unicodecsv

def dnv_registry_listing_soup(alphabetLetter, output_file_base):
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

def dnv_collect_registry_listing():
    theLetters = map(chr, range(65, 91))
    for aLetter in theLetters:
        dnv_registry_listing_soup(aLetter, 'dnv_listing')

def dnv_unify_registryListing(output_file, csvSwitch=0):
    db={}
    theLetters = map(chr, range(65, 91))
    for letter in theLetters:
        file_name = './dnv_registry_output/dnv_listing_%s.txt' % letter
        db.update(file_to_db(file_name))
    if csvSwitch:
        with open(output_file, 'w') as f:
            fields = get_all_ship_fields(db)
            csvWriter = unicodecsv.DictWriter(f, fields, encoding='utf-8')
            ships = db.keys()
            csvWriter.writeheader()
            for ship in ships:
                csvWriter.writerow(db[ship])
    else:
        db_to_file(db, './dnv_registry_output/dnv_listing.txt')

dnv_unify_registryListing('dnv_directory_list2.csv',1)