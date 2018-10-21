"""
Skeleton file for the project 1 of the LINGI2364 course.
Use this as your submission file. Every piece of code that is used in your program should be put inside this file.

This file given to you as a skeleton for your implementation of the Apriori and Depth
First Search algorithms. You are not obligated to use them and are free to write any class or method as long as the
following requirements are respected:

Your apriori and alternativeMiner methods must take as parameters a string corresponding to the path to a valid
dataset file and a double corresponding to the minimum frequency.
You must write on the standard output (use the print() method) all the itemsets that are frequent in the dataset file
according to the minimum frequency given. Each itemset has to be printed on one line following the format:
[<item 1>, <item 2>, ... <item k>] (<frequency>).
Tip: you can use Arrays.toString(int[] a) to print an itemset.

The items in an itemset must be printed in lexicographical order. However, the itemsets themselves can be printed in
any order.

Do not change the signature of the apriori and alternative_miner methods as they will be called by the test script.

__authors__ = "<write here your group, first name(s) and last name(s)>"
"""

import time

class Dataset:
    """Utility class to manage a dataset stored in a external file."""

    def __init__(self, filepath):
        """reads the dataset file and initializes files"""
        self.transactions = list()
        self.items = set()

        try:
            lines = [line.strip() for line in open(filepath, "r")]
            lines = [line for line in lines if line]  # Skipping blank lines
            for line in lines:
                transaction = list(map(int, line.split(" ")))
                self.transactions.append(transaction)
                for item in transaction:
                    self.items.add(item)
        except IOError as e:
            print("Unable to read dataset file!\n" + e)

    def trans_num(self):
        """Returns the number of transactions in the dataset"""
        return len(self.transactions)

    def items_num(self):
        """Returns the number of different items in the dataset"""
        return len(self.items)

    def get_transaction(self, i):
        """Returns the transaction at index i as an int array"""
        return self.transactions[i]


def apriori(filepath, minFrequency):
    """Runs the apriori algorithm on the specified file with the given minimum frequency"""
    dataSet = Dataset(filepath)
    def createC1(dataSet):
        '''
            create the initialied potential frequent set, which means every set has one element only
            C1 is the set that has all the elements size 1
        '''
        C1 = []
        for transaction in dataSet.transactions:
            for item in transaction:
                if [item] not in C1:
                    C1.append([item])
        # return map( frozenset, C1 )
        # return [var for var in map(frozenset,C1)]
        return [frozenset(var) for var in C1]  # transform C1 from list to frozenset

    def scanD(dataSet, potential_Frequentset, minSupport):
        '''
            calculate the support of the sets in potential_Frequentset
            return the set that meet the minsupport
            and the dictionary that has the support information of every set
        '''
        temporary = {}
        for transactions in dataSet:  # for every transaction
            for candidateSet in potential_Frequentset:  # for every candidate set，check whether it is a part of transaction
                if candidateSet.issubset(transactions):
                    temporary[candidateSet] = temporary.get(candidateSet, 0) + 1
        numItems = float(len(dataSet))
        retList = []  # []means list
        supportData = {}  # {}means dictionary
        for key in temporary:
            support = temporary[key] / numItems  # the support of every set
            if support >= minSupport:  # put the set that meet the minsupport into retList
                retList.insert(0, key)
            supportData[key] = support  # summary the support
        return retList, supportData

    def aprioriGeneration(Lk, k):
        '''
            create new potential candidate set from previous one
            k means the number of the elements in the new set
        '''
        retList = []
        lenLk = len(Lk)
        for i in range(lenLk):
            for j in range(i + 1, lenLk):
                L1 = list(Lk[i])[: k - 2];
                L2 = list(Lk[j])[: k - 2];
                L1.sort();
                L2.sort()
                if L1 == L2:
                    retList.append(Lk[i] | Lk[j])
        return retList

    def apriori(dataSet, minSupport):
        C1 = createC1(dataSet)  # create the candidate set C1
        # D = map( set, dataSet )
        # D=[var for var in map(set,dataSet)]
        dataSet = [set(var) for var in dataSet.transactions]  # transform the data into frozenset
        L1, suppData = scanD(dataSet, C1,
                             minSupport)  # create the initialied frequent set which means every set has one element only
        L = [L1]  # L should be a list of list, if not, the function aprioriGeneration can not work well anymore
        k = 2  # for next set, there would be 2 elements in it

        while (len(L[k - 2]) > 0):
            Ck = aprioriGeneration(L[k - 2], k)
            Lk, supK = scanD(dataSet, Ck, minSupport)
            suppData.update(supK)  # add the new support data
            L.append(Lk)  # add the item which fulfil the minsupport to L
            k += 1  # the number of items in the new set increased
        return L, suppData

    print("Implemented")


def alternative_miner(filepath, minFrequency):
    """Runs the alternative frequent itemset mining algorithm on the specified file with the given minimum frequency"""
    dataset = Dataset(filepath)

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

        # convert values to sets
        newD_set = {key: set(value) for key, value in newD.items()}

        return newD_set, T


    def printFrequent(state, D, theta, T, filename):
        for j in D.keys():
            # jump invalid keys (smaller that the state items)
            if j <= state[-1]:
                continue

            new_state = [*state, j]

            # build projection D|state, j = D|new_state
            Dj = {}
            for k in D.keys():
                # keys is valid if it is greater than state items
                # and more than the one considered to expand the state
                if k > j and k > state[-1]:
                    candidate = D[k] & D[j]
                    if len(candidate) >= theta:
                        Dj[k] = candidate

            for item, transactions in Dj.items():
                #print([*new_state, item][1:], " ", "({})".format(len(Dj[item]) / T))
                filename.write(str([*new_state, item][1:]) + " " + "({})".format(len(Dj[item])/T) + "\n")
                # filename.flush()
            # proceed to children
            printFrequent(new_state, Dj, theta, T, filename)

    def ECLAT(D, minFrequency, T, database):
        filename = open('plot/frequentItem_0.8_' + database, "w")
        theta = minFrequency * T

        for item, transactions in D.items():
            if len(transactions) >= theta:
                filename.write(str([item]) + " " + "({})".format(len(transactions) / T) + "\n")
        printFrequent([0], D, theta, T, filename)

        filename.close()

    import numpy as np
    D, T = verticalRepresentation(dataset)

    # cardinalities = [len(v) for v in D.values()]
    # bins, counts = np.histogram(np.log10(cardinalities))
    # print(bins, "\n", counts)

    ECLAT(D, minFrequency, T, filepath)

    print("Implemented")

if __name__ == "__main__":
    # dataset = Dataset('accidents.dat')
    # apriori('toy.dat', 1/8)
    alternative_miner('retail.dat', 0.8)

    # datasets = ['retail.dat', 'mushroom.dat','chess.dat', 'connect.dat', 'pumsb.dat']
    # datasets = ['retail.dat', 'connect.dat', 'pumsb.dat']
    #datasets = ['retail.dat']
    #for i in range(0,len(datasets)): alternative_miner(datasets[i], 0.5)





