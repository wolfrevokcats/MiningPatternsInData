import time
from frequent_itemset_miner import Dataset

t0 = time.perf_counter()
t1 = time.time()
dataset = Dataset('connect.dat')
"""Fill the dictionary with the iterations of the dataset"""
D = dict(list(enumerate(dataset.transactions, 1)))
# print('Dictionary: ', D)
""" VERTICAL REPRESENTATION: Transform the database """
# create supports list
# create list of transactions
list_items = list(dataset.items)
list_trans = list(dataset.transactions)
# create an empty list with length == number of items
newD = dict([[i,[]]for i in list_items])
for i in list_items:
    print('----- Searching transactions of item: ', i)
    for t in list_trans:
        print('--Looking at transaction: ', t)
        if t.count(i) == 1:
            # print('found element', i,'in here')
            newD[i].append([numberOfTrans for numberOfTrans, Trans in D.items() if Trans == t])
            # print('Update support: ', support[y])
            # print('Adding new transition to the dataset: ', newD[i])
        else:
            print('move forward')

# COMPUTE THE SUPPORT
support = list()
support.append([len(newD[i]) for i in list_items])
# print(support)

# CHECK:
print('Vertical Representation of the database - first case: ')
for i in list_items:
    print('Transactions database: ', newD[i], ' with support: ', len(newD[i]))
print(time.perf_counter()-t0)
print(time.time()-t1)
# COMPUTING THE FREQUENCY
# print(newD.values())
# print(newD.keys())



