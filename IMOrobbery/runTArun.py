from DataCollected import dbDNV5, dbDNV3, dbDNV7, dbDNV1, dbDNV6, dbDNV4, dbDNV2, dbDNV8

__author__ = 'TA'
'''
Methods created when working with data harvested from DNV in dnv_exchange_soup_imo.py
IMOrobery is a set of methods for collection of information about ships from the DNV GL website using Beautiful Soup
'''

def createBigList():
    '''
    A method for grabbing list of imos from a csv (excel style) and generate a python list of numbers for later processing
    run once to create a biglist.py object form imos.csv file.
    :return: a file
    '''
    from imosFileManagement import moveCSVtoPY as foo
    foo('imos.csv', 'bigList.py')

def collectFailedDNVqueries():
    '''
    a method for taking bigfile.py and checking if the imo number from bigList.py (created by createBigList()) has been processed
    :return:
    '''
    from imosFileManagement import collectFromFile
    from imosFileManagement import collectUniqueValues
    from imosFileManagement import makeNewFile

    collectedImos = []
    with open('bigfile.py','r') as f:
        for line in f:
            collectedImos.append(int(line[3:10]))
    allImos = collectFromFile('bigList2.py')
    difference = collectUniqueValues(allImos,collectedImos)

    makeNewFile('failureList.py',difference)

'''
Here I opened the bigfile.py in Sublime Text and edited the records down to db objects.
The file of 4000 records was split into eight dbDNV#.py files. Each file should contain a db={} object with list for each ship
'''
def makeMasterDNVdb(skipNones):
    '''
    a method for unifying the eight db files into one db that is returned. This is the "mega"db
    The db is not too heavy to work with
    :skipNones: a switch statement that removes items where the 'Ship name' is None
    :return: a dictionary object with the structure {imo###1:{'Ship name':'dallur1',...}, imo###2:{'Ship name':'annar dallur',...},...}
    '''
    db={}
    db.update(dbDNV1.db)
    db.update(dbDNV2.db)
    db.update(dbDNV3.db)
    db.update(dbDNV4.db)
    db.update(dbDNV5.db)
    db.update(dbDNV6.db)
    db.update(dbDNV7.db)
    db.update(dbDNV8.db)
    if skipNones:
        allKeys=db.keys()
        for akey in allKeys:
            ship = db[akey]
            if ship['Ship name'] is None:
                del db[akey]
    return db

def shipsNotInDNV():
    '''
    a method for creating a py file with imo numbers that returned Ship name = None in the mining of the DNV database.
    These ships should be processed in the second go-around in order to get further information
    :return: creates a file named imosNotInDNV.py
    '''
    from imosFileManagement import makeNewFile
    db = makeMasterDNVdb()
    allkeys=db.keys()
    imosNotInDNV=[]
    for key in allkeys:
        ship = db[key]
        if ship['Ship name'] is None:
            imosNotInDNV.append(ship['IMO id'])
    makeNewFile('imosNotInDNV.py', imosNotInDNV)

def allPossibleKeys(db):
    if None == db:
        db = makeMasterDNVdb(True)
    allkeys = db.keys() # address of all ships
    fieldKeys=[]
    for aKey in allkeys:
        ship = db[aKey]
        shipFields = ship.keys()
        for thisKey in shipFields:
            if thisKey not in fieldKeys:
                fieldKeys.append(thisKey)

    return fieldKeys

def procDNV_1():
    import csv
    db = makeMasterDNVdb(True)
    allShips = db.keys()
    allFields = allPossibleKeys()
    allFields.remove('Machinery')
    with open('eimskipaskip.csv', 'w') as f:
        testFile = csv.DictWriter(f,allFields)
        testFile.writeheader()
        for aShip in allShips:
            ship = db[aShip]
            del ship['Machinery']

            for field in allFields:
                if field not in ship.keys():
                    ship[field] = u''

            try:
                testFile.writerow(ship)
            except Exception, e:
                print str(e.message)
            print "Used %s" % aShip
    print "all done"

def procEimskipDNV():
    import csv
    from dnv_exchange.dnv_exchange_soup_imo.DataCollected.eimskipaskip_DNV import db
    allShips = db.keys()
    allFields = allPossibleKeys(db)
    allFields.remove('Machinery')
    print allPossibleKeys(db)

    with open('eimskipaskip.csv', 'w') as f:
        testFile = csv.DictWriter(f,allFields)
        testFile.writeheader()
        for aShip in allShips:
            ship = db[aShip]
            del ship['Machinery']

            for field in allFields:
                if field not in ship.keys():
                    ship[field] = ''
                else:
                    try:
                        ship[field] = ship[field].encode('utf-8')
                    except Exception, ex:
                        ship[field] = ship[field]
                        print str(ex.message)
            try:
                testFile.writerow(ship)
            except Exception, e:
                print str(e.message)
            print "Used %s" % aShip
    print "all done"

procEimskipDNV()