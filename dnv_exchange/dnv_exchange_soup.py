__author__ = 'TA'

import csv
import urllib2
import re
from bs4 import BeautifulSoup

def collectFromDNV(imoNumber, subview, itemsToFind):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    url = 'https://exchange.dnv.com/exchange/main.aspx?extool=vessel&subview=%s&imono=%s' % (subview, imoNumber)
    try:
        page = opener.open(url)
        soup = BeautifulSoup(page.read())
    except Exception, e:
        soup = 'error'
        print e.message

    returnLibrary = {'IMO id':imoNumber}

    if soup == 'error':
        returnLibrary[subview] = 'error'
        return returnLibrary
    # check if the IMO number returns a ship title, if it doesn't return a blank name
    theTitle=soup.title.text
    shipName = re.findall('[A-Z][A-Z]+', theTitle)[1:]
    if len(shipName):
        returnLibrary['Ship name'] = ' '.join(shipName)
    else:
        returnLibrary['Ship name'] = None
        return returnLibrary

    # Loop through the items to find library
    for key in itemsToFind:
        thingFound = soup.find(itemsToFind[key][0], id=itemsToFind[key][1])
        if len(thingFound.contents) != 0:
            if len(itemsToFind[key][2]):
                match=re.findall(itemsToFind[key][2], thingFound.text)
                returnLibrary[key] = match[0]
            else:
                returnLibrary[key] = thingFound.text

    return returnLibrary

def collectFromDNVtable(imoNumber, subview, itemsToFind):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    url = 'https://exchange.dnv.com/exchange/main.aspx?extool=vessel&subview=%s&vesselid=%s' % (subview, imoNumber)
    try:
        page = opener.open(url)
        soup = BeautifulSoup(page.read())
    except Exception, e:
        print e.message

    returnLibrary = {'IMO id':imoNumber}

    # check if the IMO number returns a ship title, if it doesn't return a blank name
    theTitle=soup.title.text
    shipAndPage = re.findall(r'\w+', theTitle)[2:-1]
    if shipAndPage.__contains__('Machinery'):
        theTable=soup.find('table', id=itemsToFind[0])
        tableRows=theTable.find_all('tr')

        linePack=[]
        for row in tableRows:
            oneRow=row.find_all('td')
            oneLine=[]
            for cell in oneRow:
                toAppend = cell.text
                toAppend = ' '.join(toAppend.split())
                if 'NOT SET'==toAppend:
                    toAppend=''
                oneLine.append(toAppend)
            linePack.append(oneLine)

        return linePack

summaryItemsToFind={'DNV id': ('span', 'ucMainControl_ToolContainer__ctl1_header_mDNVId', ''),
                'Ship flag': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mFlag', ''),
                'Callsign': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mSignalLetters', ''),
                'Port of Registry': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mPort', ''),
                'GWT': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mGT', ''),
                'Owner id': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mOwnerNumber', r'\d+'),
                'Owner LRF id': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mOwnerLRF', r'\d+'),
                'Net Tonnage': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mNT', ''),
                'DWT': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mDWT', ''),
                'Manager id': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mManagerNumber', r'\d+'),
                'Manager LRF id': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mManagerLRF', r'\d+'),
                'Construction Yard id': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mYardNo', ''),
                'Year built': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mBuilt', ''),
                'DNV Type': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mType', ''),
                'DNV Class': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mClass', ''),
                'Capacity': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mRegister', ''),
                'Ship Owner': ('a', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mOwner', ''),
                'Manager': ('a', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mManager', ''),
                'Construction yard': ('a', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mYard', '')
                 }

dimensionsItemsToFind = {'Length in m': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Loa', r'[-+]?\d+.?\d+'),
                   'Length between perpendiculars in m': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Lbp', r'[-+]?\d+.?\d+'),
                   'Length load label in m': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Lload', r'[-+]?\d+.?\d+'),
                   'Length of water line in m': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Lwl', r'[-+]?\d+.?\d+'),
                   'Width extreme in m': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Bext', r'[-+]?\d*.?\d+'),
                   'Depth mulded in m': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_D', r'[-+]?\d*.?\d+'),
                   'Draugth': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Draught', r'[-+]?\d*.?\d+'),
                   'Freeboard note': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Freeboard', '')
                   }

hullsummaryItemsToFind = {'Crane capacity': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_CraneCapacity', ''),
                   'Hull superstructure': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Superstructures', ''),
                   'Hull trans bulkheads': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_TransBulkheads', ''),
                   'Hull decks': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Decks', ''),
                   'Hull long bulkheads': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_LongBulkheads', ''),
                   'Hull other openings': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_OtherOpenings', ''),
                   'Hull cargo tanks': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_CargoTanks', ''),
                   'Hull side openings': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_SideOpenings', ''),
                   'Cargo max grain': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Grain', ''),
                   'Cargo max bale': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Bale', ''),
                   'Cargo max liquid': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Liquid', ''),
                   'Cargo pumps': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_Pumps', ''),
                   'Cargo pump capacity': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_PumpCapacity', ''),
                   'Cargo pump rooms': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_PumpRooms', ''),
                   'Hatchway dimensions': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_HatchwayDim', ''),
                   'Ballast capacity in m3': ('span', 'ucMainControl_ToolContainer__ctl1_tabControl__ctl1_BallastCapacity', r'[-+]?\d*.?\d+'),
                   }

machinerysummaryItems = ['ucMainControl_ToolContainer__ctl1_tabControl__ctl1_mGrid', '']

def buildMasterTable(imoID):
    masterDictionary = {}
    summaryInfo = collectFromDNV(imoID, 'summary', summaryItemsToFind)
    masterDictionary.update(summaryInfo)

    if summaryInfo['Ship name'] is not None:
        dimensions = collectFromDNV(imoID, 'dimensions', dimensionsItemsToFind)
        masterDictionary.update(dimensions)

        hullSummary = collectFromDNV(imoID, 'hullsummary', hullsummaryItemsToFind)
        masterDictionary.update(hullSummary)

        if 'DNV id' in summaryInfo:
            dnvid = summaryInfo['DNV id']
            machineTable = {'Machinery':collectFromDNVtable(dnvid, 'machinerysummary', machinerysummaryItems)}
            masterDictionary.update(machineTable)

    return masterDictionary
