import itertools
from collections import defaultdict
import numpy as np
import sys

# freq_dict: {(item): wracc}
wracc_saver = {}
# supp_dict = {(item): (supp_pos, supp_neg)}
supp_dict = {}
# wracc_dict = {wracc:[item]}
wracc_dict = {}
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
        return [d,counter]

class SearchNode:
    # constructor: each node has a reference to
    def __init__(self, name, node, dict_pos, dict_neg):
        self.name = name
        self.node = node
        self.dataset_pos = dict_pos
        self.dataset_neg = dict_neg

    def compute_support(self):
        # compute support of the nodes
        # print("----- Compute support-----")
        # 1) Get all the possible sibling of a node
        candidates_children = set(self.dataset_pos.keys()).union(set(self.dataset_neg.keys()))
        # 2) Compute support of (item+y), with y = each possible candidates children
        for item in candidates_children:
            if item in self.dataset_pos:
                pos_supp = len(set([x[0] for x in self.dataset_pos[item]]))
            else:
                pos_supp = 0

            if item in self.dataset_neg:
                neg_supp = len(set([x[0] for x in self.dataset_neg[item]]))
            else:
                neg_supp = 0

            # update the supp dictionary
            supp_dict[(*self.name, item)] = pos_supp, neg_supp
            item_wracc = compute_wracc(pos_supp, neg_supp)
            wracc_saver[(*self.name, item)] = item_wracc
            self.update_wracc_dict(item, item_wracc, k)


    def update_wracc_dict(self, item, item_wracc, k):
        # print("---- Update Frequency ----")
        # print("Method called by item ", item)
        # self = node, item = name of the node
        # combined supp already present in the freq_dict, not max length
        if item_wracc in wracc_dict.keys():
             # do the check if a subset or superset is present
            wracc_dict[item_wracc].append( (*self.name, item) )
        # max length reached
        elif len(wracc_dict) == k:
            min_wracc = min(wracc_dict.keys())
            if item_wracc > min_wracc:
                del wracc_dict[min_wracc]
                wracc_dict[item_wracc] = [ (*self.name, item) ]
        # combined supp not present, not max length
        else:
            wracc_dict[item_wracc] = [ (*self.name, item) ]


    def generate_children(self):
        # One node can generate its children
        # print("---- Generating Children ----")
        # 1) Check support of its children
        self.compute_support()
        # 2) Update freq_dict --> done directly inside compute_support each time I had something
        # 3) Take all the frequent items in freq_dict
        possible_children = set(self.dataset_pos.keys()).union(set(self.dataset_neg.keys()))
        #print("possible children: ", possible_children)
        # take them just once
        for search_element in possible_children:
            # element was not added to the frequent dictionary
            # if sum(supp_dict[(*self.name, search_element)]) < min(wracc_dict.keys()):
            threshold = (min(wracc_dict.keys())*(np.square((N+P)))/N)
            #print("threshold = ", threshold)
            #print("pos supp of ", (*self.name, search_element), " = " ,supp_dict[(*self.name, search_element)][0])
            if supp_dict[(*self.name, search_element)][0] >= threshold:
                # proceed to next iteration, without doing anithing for current value
                # if flag == true{ new_dict_pos = ...}
                new_dict_pos = self.project_dB(possible_children, search_element, self.dataset_pos)
                new_dict_neg = self.project_dB(possible_children, search_element, self.dataset_neg)

                #print("new dict pos of item = ", search_element, " = ", len(new_dict_pos))
                #print("new dict neg of item = ", search_element, " = ", len(new_dict_neg))
                if len(new_dict_pos) > 0 or len(new_dict_neg) > 0:
                    #print("search node")
                    new_name = (*self.name, search_element)
                    SearchNode(new_name, search_element, new_dict_pos, new_dict_neg).generate_children()

    def project_dB(self, flip_dic, search_term, table):
        #print("--- projected database of element: ", search_term, "---")
        new_db = {k: v for k, v in table.items() if k in flip_dic}
        # print("new_db", new_db)

        # now i have a dictionary of relevant items
        # need to check the first occurance of each trans of the search term
        # then remove all that are before the first occurance
        first_occurance = {}

        #print(" Pruning ")

        if search_term in new_db.keys():
            # Get first occurrences of element
            first_occurance = {}
            for tx, pos in new_db[search_term]:
                if tx in first_occurance:
                    # update if already there
                    first_occurance[tx] = min(first_occurance[tx], pos)
                else:
                    # add new value
                    first_occurance[tx] = pos

            newer_db = defaultdict(list)
            for item, tx_pos_list in new_db.items():
                for tx, pos in new_db[item]:
                    if tx not in newer_db[search_term] and \
                       tx in first_occurance and \
                       pos > first_occurance[tx]:
                        newer_db[item].append((tx, pos))

            return {k: v for k, v in newer_db.items() if newer_db[k] != []}

        return {}


def sequence_mining(filepath_pos, filepath_neg, k):
    global P
    global N
    [dict_pos, P] = Dataset(filepath_pos).get_v()
    [dict_neg, N] = Dataset(filepath_neg).get_v()
    #print("P = ", P)
    #print(dict_pos)
    #print("N = ", N)
    #print(dict_neg)

    empty_node = SearchNode([], '', dict_pos, dict_neg)
    empty_node.generate_children()
### main

#pos_filepath = 'positive.txt'
#neg_filepath = 'negative.txt'

# sequence_mining("reu1_acq.txt","reu2_earn.txt",k)
# sequence_mining("prot1_PKA_group15.txt","prot2_SRC1521.txt",k)

def compute_wracc(px, nx):
    return round(((P/(P+N))*(N/(P+N)))*((px/P)-(nx/N)),5)

def print_frequent(wracc_dict,supp_dict,wracc_saver):
    min_wracc = min(wracc_dict.keys())
    for (itemset) in wracc_saver.keys():
        if wracc_saver[itemset] >= min_wracc:
            print("[{}]".format(", ".join(itemset)), supp_dict[itemset][0], supp_dict[itemset][1], wracc_saver[itemset])


def main():
    global k
    pos_filepath = sys.argv[1] # filepath to positive class file
    neg_filepath = sys.argv[2] # filepath to negative class file
    k = int(sys.argv[3])
    #k = 6
    #pos_filepath = "positive.txt"
    #neg_filepath = "negative.txt"
    #pos_filepath = "reu1_acq.txt"
    #neg_filepath = "reu2_earn.txt"
    # pos_filepath = "prot1_PKA_group15.txt"
    # neg_filepath = "prot2_SRC1521.txt"

    sequence_mining(pos_filepath, neg_filepath, k)
    print_frequent(wracc_dict,supp_dict,wracc_saver)

    #print("wracc dict")
    #print(wracc_dict)
    #print("freq dict")
    #print(freq_dict)


if __name__ == "__main__":
    main()