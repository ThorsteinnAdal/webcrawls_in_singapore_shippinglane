
__author__ = 'TA'
import re
import csv
import json

def MaritimeConnectorSoup(imoNumber):
    '''
Soup module that grabs information from MarineConnection
    '''
    import urllib2
    from bs4 import BeautifulSoup

    print 'Getting data from MaritimeConncetor for IMO: %s'% imoNumber
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    # define the proper web address
    url = 'http://maritime-connector.com/ship/%s/' % imoNumber
    page = opener.open(url)
    soup = BeautifulSoup(page.read())

    # find if a valid IMO number has been found
    title = soup.text.strip().split()
    if str(imoNumber) not in title:
        print 'ship not found'
        return {'imo_id': imoNumber, 'name_s':None}

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

#print {'imo9346548':MaritimeConnectorSoup(9346548)}

def get_IMO_numbers_from_file(fileName,startIndex,endIndex):
    print 'Getting IMO numbers from file: %s' % fileName
    retList = []
    with open('.\csv_input\%s' % fileName, 'r') as f:
        ii = 0
        for line in f:
            if ii > endIndex:
                return retList
            if ii > startIndex:
                retList.append(line[:-1])
            ii+=1
    return retList
#imos = get_IMO_numbers_from_file('allIMOs.csv', 0, 12000)
#print len(imos) # = 4617


def dump_findings_to_json(nameOfOutput,start,stop):
    import time
    imos = get_IMO_numbers_from_file('allIMOs.csv', start, stop)

    fileName = '.\csv_output\%s_%s_%s.json' % (nameOfOutput, str(start), str(stop))
    ii=0
    with open(fileName, 'w') as f:
        for imo in imos:
            print 'index: %s' % str(ii)
            db = {'imo%s'%imo :  MaritimeConnectorSoup(imo)}
            f.writelines(json.dumps(db))
            f.writelines('\n')
            ii+=1
            time.sleep(0)
# dump_findings_to_json('json', 4505, 4620)

def build_database(list_of_imo_numbers):
    print 'Building database from imoNumbers'
    db ={}
    for imo in list_of_imo_numbers:
        db['imo%s' % imo] = MaritimeConnectorSoup(int(imo))

    print 'Completed building database. Total number of entries: %s' % len(db)
    return db

def get_all_fields_from_db(db):
    shipHandles = db.keys()
    allFields = []
    for ship in shipHandles:
        for aKey in db[ship]:
            if aKey not in allFields:
                allFields.append(aKey)
    return allFields

def send_db_to_CSV_file(db, fileName):
    fieldNames = get_all_fields_from_db(db)
    ships = db.keys()
    with open('.\csv_output\%s' % fileName, 'w') as f:
        outD = csv.DictWriter(f, fieldNames, dialect = 'excel')
        outD.writeheader()
        for ship in ships:
            outD.writerow(db[ship])
#dbs={'imo12344':{'name':'name1', 'imo':'imo1'}, 'imo2345':{'name':'name2','imo':'imo2', 'field':'extraField1'}, 'imo12345':{'name':'name3', 'imo':'imo3'}, 'imo23451':{'name':'name4','imos':'differentIMO', 'field':'extraField2'}}
#send_db_to_CSV_file(dbs,'test.csv')

def remove_none_values_from_db(db,keyForDropEvent,valueForDropEvent):
    ships = db.keys()
    for ship in ships:
        shipDB = db[ship]
        if keyForDropEvent in shipDB.keys():
            if shipDB[keyForDropEvent] == valueForDropEvent:
                del(db[ship])

    return db



#dbshort = {'ship1':{'imo':12345, 'Name':None},'ship2':{'imo':2222, 'Name':'Some'}}
#print remove_none_values_from_db(dbshort,'Name','Some')

def get_db_from_file(fileName):
    db = {}
    theFile = '.\csv_output\%s' % fileName
    with open(theFile,'rU') as f:
        dictRead = csv.DictReader(f, dialect='excel')
        for line in dictRead:
            db['imo%s' % line['IMO number']] = line
    return db

def add_db_to_ouputFile(db,fileName):
    newDB = get_db_from_file(fileName)
    newDB.update(db)
    theFile = '.\csv_output\%s' % fileName
    allFields = get_all_fields_from_db(newDB)
    allKeys = newDB.keys()
    with open(theFile, 'w') as f:
        csvW = csv.DictWriter(f, fieldnames=allFields, dialect='excel')
        csvW.writeheader()
        for aKey in allKeys:
            ship = newDB[aKey]
            csvW.writerow(ship)

#add_db_to_ouputFile({'new':{'Name of ship':'dallur 1', 'newField':'koppur'}},'test.csv')

def runTArun(outputFile):
    get_all_fields_from_db(db)
    imos = get_IMO_numbers_from_file('allIMOs.csv', 0, 100000) # This gets all the IMO numbers
    for i in range(0,10):
        if i < len(imos):
            print 1


'''
imos = get_IMO_numbers_from_file('allIMOs.csv',0,10)
dbFull = build_database(imos)
dbTrimmed = remove_none_values_from_db(dbFull,'Name of ship',None)
send_db_to_CSV_file(dbTrimmed, 'tiny.csv')
'''



