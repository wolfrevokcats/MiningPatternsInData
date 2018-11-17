import re


class Dataset:
    """Utility class to manadirge a dataset stored in a external file."""

    def __init__(self, filepath):
        """reads the dataset file and initializes files"""
        self.transactions = list()
        self.items = set()
        try:
            lines = [line.strip() for line in open(filepath, "r")]
            lines = [line for line in lines if line]  # Skipping blank lines
            for line in lines:
                transaction = list(map(str, line.split(" ")))
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

    def get_dict(self):
        d = {}
        l = []
        for i in range(len(self.transactions)):
            transaction = int(self.transactions[i][1])
            # All elements not at the start of the transaction
            if transaction != 1:
                # If the element appears for the first time in the search
                if self.transactions[i][0] not in d:
                    # create a list with the first occurrence
                    d[self.transactions[i][0]] = [transaction]
                else:
                    # append the position of the element to the list
                    d[self.transactions[i][0]].append(transaction)
                # last element
                if i == len(self.transactions)-1:
                    l.append(d)
            # All first elements
            else:
                if d != {}:
                    l.append(d)
                d = {}
                d[self.transactions[i][0]] = [transaction]
        return l

    def get_v(self):
        d = {}
        l = []
        counter = 0
        for i in range(len(self.transactions)):
            transaction = (self.transactions[i])
            # print(transaction)
            id = int(transaction[1])
            # print(id)
            # All elements not at the start of the transaction
            if id == 1:
                counter += 1
            if transaction[0] not in d:
                # print(transaction[0])
                # create a list with the first occurrence
                d[transaction[0]] = [(counter, id)]
                # print(d[transaction[0]])
            else:
                # append the position of the element to the list
                d[transaction[0]].append((counter, id))
                # print(d[transaction[0]])
        return d

def sequence_mining(filepath1,filepath2,k):
    dataset_pos = Dataset(filepath1)
    dataset_neg = Dataset(filepath2)

    dict_pos = dataset_pos.get_v()
    dict_neg = dataset_neg.get_v()

    print("--- Positive dictionary ---")
    print(dict_pos)
    print("--- Negative dictionary ---")
    print(dict_neg)



    def update_freqDict(newFreq,newItem,freq_dict,k):
        # which are the parameters?
        # create somewhere else the freq_dict

        # k = number of entries of the dictionary!!
        # dictionary of the k-most frequent items: freq_dict = {<freq_1,item_1>...<freq_k,item_k>}
        # get last element: freq = list(freq.items()), freq[-1]
        # get the smallest frequency among the one in the dictionary: freq[-1][0]
        return ""



    # non esiste minfrequency ma un dizionario di k frequenze
    #
    #def SPADE(D,minfFrequency):
    #    # minFrequency == k
    #    theta = minFrequency * T
    #    for item, transactions in D.items():
    #        if len(transactions) >= theta:
    #            print([item], len(transactions) / T)
    #    printFrequent([0], D, theta, T)

    #D, T = verticalRepresentation(dataset)
    #ECLAT(D, minFrequency, T)


if __name__ == '__main__':
    # Possible tests:
    # prot1_PKA_group15.txt
    # prot2_SRC1521.txt
    # reu1_acq.txt
    # reu2_earn.txt

    sequence_mining("positive.txt","negative.txt",2)

