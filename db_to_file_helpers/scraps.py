__author__ = 'thorsteinn'
import json
import os


a = [1, 2, 3, 4, u'imo1', u'imo2', u'imo3', u'imo4']
jsonOutput = json.dumps(a)
print jsonOutput
aa = json.loads(jsonOutput)
print aa
print a == aa

print os.getenv("HOME")
print os.path.curdir