import time
from frequent_itemset_miner import Dataset
import itertools

t0 = time.perf_counter()
t1 = time.time()
dataset = Dataset('toy.dat')
"""Fill the dictionary with the iterations of the dataset"""
D = dict(list(enumerate(dataset.transactions, 1)))
# print('Dictionary: ', D)
""" VERTICAL REPRESENTATION: Transform the database """
# create supports list
# create list of transactions
list_items = list(dataset.items)
list_trans = list(dataset.transactions)
T = len(list_trans)
"""Vertical Representation"""
# create an empty list with length == number of items
newD ={}
for i in D:     #run through all trans in dict
    # print(i)
    for j in D[i]:  #run through the items in esch trans
        if j not in newD:
            newD[j] = [i]
        else:
            newD[j].append(i)

#print(newD)
# COMPUTE THE SUPPORT and frequency
y = 0
support, frequency = [],[]
for i in list_items:
    support.append(len(newD[i]))
    frequency.append(support[y]/T)
    y = y+1
print(support)

# COMPUTE THE FREQUENCY
print('Frequency vector: ', frequency)

# CHECK:
print('Vertical Representation of the database - first case: ')
y = 0
for i in list_items:
    print('Item : ', i, 'is present in the transactions ', newD[i], ' with support: ', support[y], 'and frequency', frequency[y])
    y = y+1
print(time.perf_counter()-t0)
print(time.time()-t1)

print(newD.keys())
print(newD.values())
print(newD)
# DFS
k = 0
for i in newD:  # run thought the new dictionary
    for j in newD:
        if len(list(set(newD[i])&set(newD[j]))) == 0:
            print('empty list')
        else:
            print('intersection of item', i , 'with element', j, 'is: ', list(set(newD[i])&set(newD[j])))


lst = set(list(itertools.combinations(newD.keys(),4)))




