__author__ = 'TA'

import re

listOfShips = [9086801, 9238806, 9384198, 8914568, 8914556, 9086796, 9323089, 2332197, 9641314]

def makeNewFile(F,A):
    """
    creates a file from a list that is provided
    :param file: a file in the folder
    :param list: a python list of integers i.e. [1,2,3,5]
    """
    with open(F,'w') as f:
        for item in A:
            f.write(str(item)+'\n')

def collectFromFile(F):
    """
A simple method to collect all integers from a file and return a list-object
    :param file: a file on the system, preferably made by makeNewFile(file,list)
    :return: list of integers
    """
    returnList=[]
    with open(F,'r') as f:
        for line in f:
            returnList.append(int(line[:-1]))
    return returnList

def addToFile(F,A):
    """
A method for adding a list of integers to a file
    :param file: a file that exists, e.g. made by makeNewFile(file,list)
    :param list: a list of integers
    """
    with open(F,'a') as f:
        for item in A:
            f.write(str(item)+'\n')

def removeFromFile(F,A):
    """
a method for removing all instances of a number in a file
    :param file: a file that exists made by makeNewFile(file,list)
    :param A: a list of integers (or a single integer in a list)
    """
    filecontent = collectFromFile(F)
    for item in A:
        while item in filecontent:
            filecontent.remove(item)
    makeNewFile(F, filecontent)

def collectUniqueValues(listA,listB):
    uniques=[]
    if len(set(listA))>len(set(listB)):
        A = list(set(listA))
        B = list(set(listB))
    else:
        B = list(set(listA))
        A = list(set(listB))
    for value in A:
        if value not in B:
            uniques.append(value)
    return uniques

def removeDuplicatesFromFile(F):
    fileContent = collectFromFile(F)
    fileContent = list(set(fileContent))
    makeNewFile(F, fileContent)

def addUniqueToFile(F,A):
    """
A method for adding new values from a list to a file
    :param file: a file preferably made by makeNewFile(F,A)
    :param list: a list of integer values (imos)
    """
    fileContent = collectFromFile(F)
    for item in A:
        if item not in fileContent:
            addToFile(F, [item])

def moveCSVtoPY(csvFile_in,pyFile_out):
    bunch = []
    with open(csvFile_in, 'r') as f:
        for line in f:
            toAppend = re.findall(r'\d+', line)
            bunch.append(int(toAppend[0]))
    makeNewFile(pyFile_out, bunch)