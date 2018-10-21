import time
from frequent_itemset_miner import Dataset
import itertools
import numpy as np


def verticalRepresentation(dataset):
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

    return newD, T


def printFrequent(state, D, theta, T):
    valid_keys = [k for k in D.keys() if k > state[-1]]
    for j in valid_keys:
        new_state = [*state, j]

        # build projection D|state, j = D|new_state
        Dj = {}
        for k in valid_keys:
            if k > j:
                candidate = list(set(D[k]) & set(D[j]))
                if len(candidate) >= theta:
                    Dj[k] = candidate

        for item, transactions in Dj.items():
            print([*new_state, item][1:], (len(Dj[item]))/T)

        # proceed to children
        printFrequent(new_state, Dj, theta,T)


def ECLAT(D, theta, T):
    for item, transactions in D.items():
        if len(transactions) >= theta:
            print([item], len(transactions)/T)
    printFrequent([0], D, theta, T)

"""----------------------- MAIN --------------------"""
if __name__ == "__main__":
    dataset = Dataset('accidents.dat')
    D,T = verticalRepresentation(dataset)
    ECLAT(D, T*0.8, T)