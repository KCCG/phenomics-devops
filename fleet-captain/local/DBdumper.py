# from random import randrange
#
# import json
#
#
# mil = [x for x in range(1, 250000)]
# items = []
# items.append("PMID,count\n")
# for x in mil:
#     items.append("{},{}\n".format(x*10, randrange(0, 10)))
#
# with open('test2.csv', 'w') as f:
#     f.writelines(items)gs