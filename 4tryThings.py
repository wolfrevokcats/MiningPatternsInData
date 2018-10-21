import time
from frequent_itemset_miner import Dataset
import itertools
import numpy as np

def verticalRepresentation(dataset):
    t0 = time.perf_counter()
    t1 = time.time()
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
    newD = {}
    for i in D:  # run through all trans in dict
        # print(i)
        for j in D[i]:  # run through the items in esch trans
            if j not in newD:
                newD[j] = [i]
            else:
                newD[j].append(i)
    y = 0
    support, frequency = [], []
    for i in list_items:
        support.append(len(newD[i]))
        frequency.append(support[y] / T)
        y = y + 1

    print(time.perf_counter() - t0)
    print(time.time() - t1)
    return newD,T

# do all the possible combinations
# compute the support of every combinarion


if __name__ == "__main__":
    dataset = Dataset('toy.dat')
    D,T = verticalRepresentation(dataset)
    print(D)