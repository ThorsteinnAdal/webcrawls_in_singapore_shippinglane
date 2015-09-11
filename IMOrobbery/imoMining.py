__author__ = 'TA'

import imosFileManagement
from dnv_exchange.dnv_exchange_soup_imo import buildMasterTable

imoList = imosFileManagement.collectFromFile('eimskipaskip.py')

with open('eimskipaskip_DNV.py','w') as f:
    for ship in imoList:
        theLine = 'imo%s = %s \n' % (ship, buildMasterTable(ship))
        f.write(theLine)
        print "imo%s completed" % str(ship)

