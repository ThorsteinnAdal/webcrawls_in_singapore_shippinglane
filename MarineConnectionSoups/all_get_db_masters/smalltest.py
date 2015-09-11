__author__ = 'thorsteinn'

from db_to_file_helpers.jsonDicts_to_file import file_to_db, db_to_file
import re

def cycle():

    with open('mc_db_master.txt') as f:
        all_lines = f.readlines()
        print len(all_lines)

    db = file_to_db('mc_db_master.txt')
    ships = db.keys()

    print len(ships)
    print len(set(ships))

    nums = []
    for ship in ships:
        nums.append(re.findall(r'\d\d*', ship)[0])

    print len(nums)
    print len(set(nums))
    nums_set = list(set(nums))

    ind = 0
    for num in nums_set:
        ship = ships[ind]
        ships.remove(ship)
        nums.remove(num)
        ind += 1
    print ships
    print nums

    print '='*20



cycle()

