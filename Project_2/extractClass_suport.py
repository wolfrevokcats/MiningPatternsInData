import re
from collections import Counter



class Dataset:
    """Utility class to manadirge a dataset stored in a external file."""

    def __init__(self, filepath):
        """reads the dataset file and initializes files"""
        self.transactions = list()
        self.items = set()
        self.d = {}
        self.l = []
        self.column = []
        try:
            self.column = [x.split(' ')[0] for x in open(filepath).readlines()]
            self.column = [col for col in self.column if col]
            #print(self.column)
            lines = [line.strip() for line in open(filepath, "r")]
            lines = [line for line in lines if line]  # Skipping blank lines
            for line in lines:
                transaction = list(map(str, line.split(" ")))
                self.transactions.append(transaction)
                for item in transaction:
                    self.items.add(item)

        except IOError as e:
            print("Unable to read dataset file!\n" + e)

    def get_column(self):
        return self.column

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

    def get_counter(self):
        return ""

if __name__ == '__main__':
    d = Dataset("negative.txt")
    l = d.get_dict()
    #print(l)
    supp = Counter()
    key = supp(d.get_column()).keys()
    val = supp(d.get_column()).values()
    # [l,k] = d.get_col()
    # prot1_PKA_group15.txt
    # prot2_SRC1521.txt
    # reu1_acq.txt
    # reu2_earn.txt

