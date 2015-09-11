__author__ = 'thorsteinn'

import urllib2
from bs4 import BeautifulSoup

def setup_items_to_find(sub_view):
    return_db = {}
    if sub_view == 'record_vesseldetailsprinparticular':
        return_db['Designation'] = {'table_type': 'two_column_table',  }
    'Designation', 'Categories', 'Anchor Equipment', 'Other Info', 'Principal Characteristics'


def abs_soup(abs_id='09180808', sub_view='record_vesseldetailsprinparticular'):

    print 'Getting %s from abs for abs_id: %s' % (sub_view, abs_id)
    print len(abs_id)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    # define the proper web address
    url = 'https://www.eagle.org/safenet/record/%s?Classno=%s&Accesstype=PUBLIC' % (sub_view, abs_id)
    # example

    # set up the return library:
    db = {'abs_id': abs_id}

    # try to open the page
    try:
        page = opener.open(url)
        soup = BeautifulSoup(page.read())
    except Exception, mess:
        db['name_s'] = None
        db['pageMessage'] = mess.message
        return db

    # check if a valid page was found. This could be handled with httpException in the urllib2
    validPage = soup.find_all('title')
    if validPage[0].text == 'ABS Record':
        print "A valid ship was found"
    elif validPage[0] == 'Error':
        print "The class number was incorrect (check padding to length = 8)"
    else:
        db['pageMessage'] = validPage[0]
        return db

    # header table -- contains the ship name
    header_table = soup.find_all('table', attrs={'class': 'innertable'})
    header_rows = header_table[2].find_all('tr')
    header_fields = header_rows[0].find_all('td')
    header_values = header_rows[1].find_all('td')

    # get the information from the header table
    for item in range(len(header_fields)):
        field = header_fields[item].contents[0].strip()  # contains all the field names in the header
        value = header_values[item]  # contains all the value items in the header
        if field:
            db[field] = value.contents[0].strip()
        else:
            break

    data_tables = soup.find_all('table', attrs={'class':'tableforms'})
    # the first data table is the holder.
    # specific to summary page:

    single_column_tables = ['ABS Class Notations', 'Functions',
                        'International code for the security of the ships and of port facilities (ISPS Code), ABS Security Notation']
    two_column_tables = ['Designation', 'Categories', 'Anchor Equipment', 'Other Info', 'Principal Characteristics']

    for i in range(len(data_tables)):
        data_table = data_tables[i]
        table_title = data_table.contents[1].text.strip()

        if table_title in two_column_tables:
            titles = data_table.find_all('td', attrs={'class': 'row2bold', 'width': '50%'})
            values = data_table.find_all('td', attrs={'class': 'row1', 'width': '40%'})
            for index in range(len(titles)):
                title = titles[index].contents[0].strip()
                value = values[index]
                if len(value) == 0:
                    db[title] = None
                else:
                    db[title] = value.contents[0].strip()

        elif table_title in single_column_tables:
            print table_title
            values = data_table.find_all('td', attrs={'class': 'row1', 'width': '40%'})
            print 1
            pass
    return db

print abs_soup()

'''
    # find if a valid IMO number has been found
    title = soup.text.strip().split()
    if str(imoNumber) not in title:
        print 'ship not found'
        return {'IMO number': imoNumber, 'Name of ship':None}

    # passed title find the rows in the data table
    t = soup.find_all('table', attrs = {'class':'ship-data-table'})
    tr = t[0].find_all('tr')

    # break the rows into a dictionary
    retDict = {}
    for aRow in tr:
        head = aRow.find('th').text.encode('utf-8')
        val = aRow.find('td').text.encode('utf-8')

        # former names is a list of the form "SOMESHIP until 2010 Apr..."
        if 'Former names' == head:
            val = re.findall(r'\w+ until \d+ \w\w\w' , val)

        # mass names are given as "2939 tons" form
        elif 'tons' in val.split():
            val = val.split()[0]
        retDict[head] = val

    print 'complete'
    return retDict

'''