__author__ = 'thorsteinn'

def factor_table_into_db(listOfLists, idBase = 'row'):
    # assume that the first row is the titles
    db = {}
    titles = listOfLists[0]
    remainingTable = listOfLists[1:]
    rowCount = 1
    for row in remainingTable:
        row_id = idBase + str(rowCount)
        temp_db = {}
        for i in range(len(titles)):
            temp_db.update({titles[i]: row[i] if row[i] else None})
        db.update({row_id: temp_db})
        rowCount +=1
    return db

def test_factor_table_into_db():
    sampleTable = [['word_1', 'word_2', 'word_3', 'word_4'],
                   ['head', 'shoulders', 'knees', 'toes'],
                   ['head', 'shoulders', 'knees', 'toes'],
                   ['eyes', 'ears', 'mouth', 'nose'],
                   ['head', 'shoulders', 'knees', 'toes'],
                   ['knees', 'toes', u'', '']]
    print factor_table_into_db(sampleTable)
