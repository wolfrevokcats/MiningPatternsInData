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


class Dataset:
    """Utility class to manage a dataset stored in a external file."""

    def __init__(self, filepath):
        """reads the dataset file and initializes files"""
        self.transactions = list()
        self.items = set()
        self.counter = {}
        try:
            lines = [line.strip() for line in open(filepath, "r")]
            lines = [line for line in lines if line]  # Skipping blank lines
            for line in lines:
                transaction = list(map(int, line.split(" ")))
                self.transactions.append(transaction)
                for item in transaction:
                    self.items.add(item)
                    if item not in self.counter:
                        self.counter[item] = 1
                    else:
                        self.counter[item] += 1

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
    # """Runs the apriori algorithm on the specified file with the given minimum frequency"""
    # TODO: implementation of the apriori algorithm

    dataSet = Dataset(filepath)

    C1 = createC1(dataSet)
    dataSet = [set(var) for var in dataSet.transactions]  # transform the data into frozenset
    L1, suppData = scanD(dataSet, C1,
                         minFrequency)  # create the initialied frequent set which means every set has one element only
    L = [
        L1]  # L has 2, 3, 4 now     # L should be a list of list, if not, the function aprioriGeneration can not work well anymore
    k = 2  # for next level of set, there would be 2 elements in it

    while (len(L[k - 2]) > 0):
        Ck = aprioriGeneration(L[k - 2], k)
        Lk, supK = scanD(dataSet, Ck, minFrequency)
        suppData.update(supK)  # add the new support data
        L.append(Lk)  # add the item which fulfil the minsupport to L
        k += 1  # the number of items in the new set increased
    return L, suppData

def createC1(dataSet):
    '''
        create the initialied potential frequent set, which means every set has one element only
        C1 is the set that has all the elements size 1
    '''
    C1 = []
    for transaction in dataSet.transactions:
        for items in transaction:
            if [items] not in C1:
                C1.append([items])
    # return map( frozenset, C1 )
    # return [var for var in map(frozenset,C1)]
    return [frozenset(var) for var in C1]  # transform C1 from the list to a frozenset


def scanD(dataSet, potential_Frequentset, minSupport):
    '''
        calculate the support of the sets in potential_Frequentset
        return the set that meet the minsupport
        and the dictionary that has the support information of every set
    '''
    temporary = {}
    # print("the type of ")
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
            # print ("this is List for now", retList)
            # print("#######################################")

            sets = list(key)
            sets.sort()
            # L = list(sets)
            # for x in sets:
            #     print( x )
            print(sets, "(", supportData[key], ")")
    # print("************************",type(temporary[0]))
    # print([list(x) for x in key])
    # print ("***************")
    # print (retList)
    return retList, supportData


def aprioriGeneration(Lk, k):
    '''
        create new potential candidate set from the previous one
        k means the number of the elements in the new set
    '''
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[
                 : k - 2];  # minimize the number of generating items by just considering whether the subsets shared items
            L2 = list(Lk[j])[: k - 2];
            L1.sort();
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList




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

        print("newd")
        print(newD)
        return newD, T


    def printFrequent(state,dataset,D,theta,T):
        valid_keys = [k for k in D.keys() if k > state[-1] and dataset.counter[k] >= theta]
        print("valid keys")
        print(valid_keys)
        for j in valid_keys:
            new_state = [*state, j]
            print("new state")
            print(new_state)
            # build projection D|state, j = D|new_state
            Dj = {}
            for k in valid_keys:
                print("considered key in valid_key")
                print(k)
                if k > j:
                    candidate = list(set(D[k]) & set(D[j]))
                    print("candidate")
                    print(candidate)
                    if len(candidate) >= theta:
                        Dj[k] = candidate
                        print("Dj[k]")
                        print(Dj[k])

            for item, transactions in Dj.items():
                print([*new_state, item][1:], (len(Dj[item])) / T)

            # proceed to children
            printFrequent(new_state, dataset, Dj, theta, T)

    def ECLAT(dataset, D, minFrequency, T):
        theta = minFrequency*T
        print(dataset.counter)
        for item in dataset.counter:
            if dataset.counter[item] >= theta:
                print([item], dataset.counter[item]/ T)
        printFrequent([0], dataset, D, theta, T)


    D, T = verticalRepresentation(dataset)
    ECLAT(dataset, D, minFrequency, T)

    print("Implemented")

if __name__ == "__main__":
    #dataset = Dataset('accidents.dat')
    #apriori('toy.dat', 1/8)
    alternative_miner('toy.dat',1/8)


