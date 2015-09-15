__author__ = 'thorsteinn'

import csv
import urllib2
import re
import json
from bs4 import BeautifulSoup

def map_bwi_page(country, port):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    url = 'http://www.bunkerworld.com/prices/port/{c}/{p}/'.format(c = country, p = port)

    page = opener.open(url)

    soup = BeautifulSoup(page.read(), 'html.parser')

    fuelHeaders = soup.find_all('div', {'class':"content_block_title"})

    db = {'table0':{'fuel:':'IFO380','iso':'RMG380 RMH380', 'report':'daily','table':[]},
          'table1':{'fuel:':'IFO180','iso':'RME180 RMF180', 'report':'daily','table':[]},
          'table2':{'fuel:':'MGO','iso':'DMA DMX', 'report':'daily','table':[]},
          'table3':{'fuel:':'LSMGO','iso': "0.1% sulfur", 'report':'daily','table':[]},
          'table4':{'fuel:':'IFO380','iso':'RMG380 RMH380', 'report':'monthly','table':[]},
          'table5':{'fuel:':'IFO180','iso':'RME180 RMF180', 'report':'monthly','table':[]},
          'table6':{'fuel:':'MGO','iso':'DMA DMX', 'report':'monthly','table':[]},
          'table7':{'fuel:':'LSMGO','iso': "0.1% sulfur", 'report':'monthly','table':[]},
          'table8':{'fuel:':'IFO380','iso':'RMG380 RMH380', 'report':'30 day','table':[]},
          'table9':{'fuel:':'IFO180','iso':'RME180 RMF180', 'report':'30 day','table':[]},
          'table10':{'fuel:':'MGO','iso':'DMA DMX', 'report':'30 day','table':[]},
          'table11':{'fuel:':'LSMGO','iso': "0.1% sulfur", 'report':'30 day','table':[]}}


    tables = soup.find_all('table', {'class':"item_table row_borders"})

    this_table = []
    index = 0

    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            this_table.append([ele for ele in cols if ele]) # Get rid of empty values
        db['table%s'% index]['table'] = this_table
        data[approved_headers[index]] = this_table
        this_table = []
        index +=1

    return db


print map_bwi_page('nl', 'rtm') #others Singapore sg/sin/, Houston us/hou/, Fujairah ae/fjr/
