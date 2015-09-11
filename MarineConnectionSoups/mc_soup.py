__author__ = 'thorsteinn'
import urllib2
from bs4 import BeautifulSoup
import re
import sys

def mc_soup(imoNumber):
    '''
Soup module that grabs information from MarineConnection
    '''

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    # define the proper web address
    try:
        url = 'http://maritime-connector.com/ship/{0:07d}/'.format(imoNumber)
    except ValueError, me:
        print "ValueError: The number {imo_id} could not be formatted.\n{message}".format(
            imo_id=imoNumber,
            message=me.message
        )
        return {'name_s': 'error'}
    try:
        page = opener.open(url)
    except urllib2.HTTPError, me:
        print "calling {imo_id} gave the error code: {code} : {message}. Returning code 'blank'".format(
            imo_id=imoNumber,
            code=me.code,
            message=me.message
        )
        return {'name_s': 'error'}
    except urllib2.URLError, me:
        print "Failed to reach server. Reason: {reason}".format(
            reason=me.reason
        )
        return sys.exit(status=123)

    soup = BeautifulSoup(page.read())

    # find if a valid IMO number has been found
    title = soup.text.strip().split()
    if str(imoNumber) not in title:
        print 'ship not found'
        return {'imo_id': imoNumber, 'name_s': None}

    # passed title find the rows in the data table
    t = soup.find_all('table', attrs={'class': 'ship-data-table'})
    tr = t[0].find_all('tr')

    # break the rows into a dictionary
    retDict = {}
    for aRow in tr:
        head = aRow.find('th').text
        val = aRow.find('td').text

        # former names is a list of the form "SOMESHIP until 2010 Apr..."
        if 'Former names' == head:
            val = re.findall(r'\w+ until \d+ \w\w\w', val)

        # mass names are given as "2939 tons" form
        elif 'tons' in val.split():
            val = val.split()[0]
        retDict[head] = val

    return retDict
