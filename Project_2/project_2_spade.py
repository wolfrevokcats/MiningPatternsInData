import itertools
from copy import deepcopy

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

    def get_v(self):
        d = {}
        counter = 0
        for i in range(len(self.transactions)):
            transaction = (self.transactions[i])
            # take the number close to the letter == position identifier
            id = int(transaction[1])
            symbol = transaction[0]
            if id == 1:
                # counter == number of transaction
                counter += 1
            if symbol not in d:
                d[symbol] = [(counter, id)]
            else:
                d[symbol].append((counter, id))
        return d

# freq_dict: {max_freq:[item]}
freq_dict = {}
# support = {(item): (supp_pos, supp_neg)}
supp_dict = {}

class SearchNode:
    # constructor: each node has a reference to
    def __init__(self,name,node,dict_pos,dict_neg):
        self.name = name
        self.node = node
        self.dataset_pos = dict_pos
        self.dataset_neg = dict_neg

    def compute_support(self):
        # compute support of the nodes

        # 1) Get all the possible sibling of a node
        candidates_children = set(self.dataset_pos.keys()).union(set(self.dataset_neg.keys()))
        # 2) Compute support of (item+y), with y = each possible candidates children
        for item in candidates_children:
            pos_supp = set()
            neg_supp = set()
            if item in self.dataset_pos:
                # item in pos dataset
                for occurr in self.dataset_pos[item]:
                    # screening its occurrences
                    pos_supp.add(occurr[0])
            else:
                # item in neg dataset
                for occurr in self.dataset_neg[item]:
                    # screening its occurrences
                    neg_supp.add(occurr[0])
            # update the supp dictionary
            supp_dict[tuple(self.name + [item])] = (len(pos_supp),len(neg_supp))
            # update the freq_dict
            self.update_freq_dict(item, len(pos_supp)+len(neg_supp), k)

    def update_freq_dict(self, item, item_support, k):
        # self = node, item = name of the node
        # combined supp already present in the freq_dict, not max length
        if item_support in freq_dict:
            freq_dict[item_support].append(self.name + ([item]))
        # max length reached
        elif len(freq_dict) == k:
            min_freq = min(freq_dict.keys())
            if item_support > min_freq:
                del freq_dict[min_freq]
                freq_dict[item_support] = [self.name + ([item])]
        # combined supp not present, not max length
        else:
            freq_dict[item_support] = [self.name + ([item])]

    def gerenate_children(self):
        # One node can generate its children

        # 1) Check support of its children
    #    self.compute_support()
        # 2) Update freq_dict --> done directly inside compute_support each time I had something
        # 3) Take all the frequent items in freq_dict
        possible_children = [items for freq, items in freq_dict.items()]
        # take just the names
        possible_children = set([names[-1] for names in list(itertools.chain.from_iterable(possible_children))])
        print(possible_children)
        # take them just once
        # 4) Generate all the combinations
        #for child in possible_children:
        # 5) Look if there is a projected database of child

    def project_dB(self, freq_dict, item, dataset):
        # 1) Release a copy of the dataset
        temp_dict = deepcopy(dataset)

        # 2) Take just the items in dataset that are frequent (inside freq_dict)
        temp_dict = {key:value for key,value in temp_dict.items() if key in freq_dict}
        print("temp dict", temp_dict)

        # 3) Get first occurrences
        if item in temp_dict.keys():
            self.get_first()

    def get_first(self, itemset, dataset):
        first_occurr = {}
        for iter in range(len(dataset[itemset])):
            key = dataset[itemset][iter][0]
            if key not in first_occurr:
                # transaction not present
                first_occurr[key] = dataset[itemset][iter][1]
            else:
                # transaction is present
                # updating the position
                if dataset[itemset][iter][1] < first_occurr[key]:
                    first_occurr[key] = dataset[itemset][iter][1]
        return first_occurr


def sequence_mining(filepath_pos,filepath_neg,k):
    dict_pos = Dataset(filepath_pos).get_v()
    dict_neg = Dataset(filepath_neg).get_v()
    print("Positive dataset")
    print(dict_pos)
    print("Negative dataset")
    print(dict_neg)


    myNode = SearchNode('A', '', dict_pos, dict_neg)



    """def print_frequent(freq_dict, supp_dict):
        for kmost in freq_dict.values():
            for value in kmost:
                print(str(j), str(supp_dict[tuple(value)][0]), str(supp_dict[tuple(value)][1]),str(supp_dict[tuple(value)][0] + supp_dict[tuple(value)][1]))
    print_frequent(freq_dict,supp_dict)"""
    print(freq_dict)

if __name__ == '__main__':
    # Possible tests:
    # prot1_PKA_group15.txt
    # prot2_SRC1521.txt
    # reu1_acq.txt
    # reu2_earn.txt
    global k
    # sequence_mining("reu1_acq.txt","reu2_earn.txt",600)
    k = 6
    # sequence_mining("prot1_PKA_group15.txt","prot2_SRC1521.txt",5)

    sequence_mining("positive.txt", "negative.txt",k)

