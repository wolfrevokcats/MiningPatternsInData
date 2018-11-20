import itertools
from copy import deepcopy
from collections import defaultdict


# freq_dict: {max_freq:[item]}
freq_dict = {}
# support = {(item): (supp_pos, supp_neg)}
supp_dict = {}
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

class SearchNode:
    # constructor: each node has a reference to
    def __init__(self, name, node, dict_pos, dict_neg):
        self.name = name
        self.node = node
        self.dataset_pos = dict_pos
        self.dataset_neg = dict_neg

    def compute_support(self):
        # compute support of the nodes
        print("----- Compute support-----")
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
            print("supp_dict")
            print(supp_dict)
            # update the freq_dict
            total_supp = len(pos_supp)+len(neg_supp)
            self.update_freq_dict(item, total_supp , k)

    def update_freq_dict(self, item, item_support, k):
        print("---- Update Frequency ----")
        print("Method called by item ", item)
        # self = node, item = name of the node
        # combined supp already present in the freq_dict, not max length
        if item_support in freq_dict.keys():
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
        print("freq_dict")
        print(freq_dict)

    def generate_children(self):
        # One node can generate its children
        print("---- Generating Children ----")
        # 1) Check support of its children
        self.compute_support()
        # 2) Update freq_dict --> done directly inside compute_support each time I had something
        # 3) Take all the frequent items in freq_dict
        possible_children = [items for freq, items in freq_dict.items()]
        # take just the names
        # 4) Generate all the combinations
        possible_children = [names[-1] for names in list(itertools.chain.from_iterable(possible_children))]
        possible_children = set(possible_children)
        print("possible_children")
        print(possible_children)
        # take them just once
        print("here")
        for search_element in possible_children:
            print("here2")
            if self.dataset_pos != {} and self.dataset_neg != {}:
                print("here3")
                new_dict_pos = self.project_dB(possible_children, search_element, self.dataset_pos)
                new_dict_neg = self.project_dB(possible_children, search_element, self.dataset_neg)
            elif self.dataset_pos == {} and self.dataset_neg != {}:
                print("here4")
                new_dict_pos = {}
                new_dict_neg = self.project_dB(possible_children, search_element, self.dataset_neg)
            elif self.dataset_pos != {} and self.dataset_neg == {}:
                print("here5")
                new_dict_pos = self.project_dB(possible_children, search_element, self.dataset_pos)
                new_dict_neg = {}
            else:
                print("here6")
                return
            print("search node")
            SearchNode(self.name + [search_element], search_element, new_dict_pos, new_dict_neg).generate_children()

    def project_dB(self, set_items, element, dataset):
        print("---- Building Projected Database ----")
        # 1) Release a copy of the dataset
        temp_dict = deepcopy(dataset)

        # 2) Take just the items in dataset that are frequent (inside freq_dict)
        # temp_dict = {item: [list of occurrences]} just for items with
        temp_dict = {key:value for key,value in temp_dict.items() if key in set_items}
        print("temp dict", temp_dict)

        # 3)
        print(" Pruning ")
        prune_dataset = defaultdict(list)
        if element in temp_dict.keys():
            # Get first occurrences of element
            first_occurr = self.get_first(element, dataset)
            # insert in prune_dataset all the not first occurrences of element
            prune_dataset = {element: list(set(dataset[element]).difference(set(list(first_occurr.items()))))}
            # the possible candidates
            possible_candidates = [x for x in temp_dict.keys() if x != element]
            # possible_candidates = list(set_items)
            print("poss cand", possible_candidates)
            for other_items in possible_candidates:
                for values in dataset[other_items]:
                    trans, pos = values
                    if trans in first_occurr:
                        # if the trans is present: other_items comes after itemset
                        if pos > first_occurr[trans]:
                            # print("This occ ", (trans, first_occurr_POS[trans]), "before this", (trans, pos))
                            if other_items not in prune_dataset:
                                prune_dataset[other_items] = [(trans, pos)]
                            else:
                                prune_dataset[other_items].append((trans, pos))
        for key in prune_dataset.keys():
            return {item:occurrences for item,occurrences in prune_dataset.items() if prune_dataset[k] != []}
        return {}

    def get_first(self, itemset, dataset):
        print("--- Get first ---")
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
    #print("Positive dataset")
    #print(dict_pos)
    #print("Negative dataset")
    #print(dict_neg)


    empty_node = SearchNode([], '', dict_pos, dict_neg)
    empty_node.generate_children()

def print_frequent(freq_dict, supp_dict):
    print("Printing")
    for kmost in freq_dict.values():
        for value in kmost:
            print(str(value), str(supp_dict[tuple(value)][0]), str(supp_dict[tuple(value)][1]),str(supp_dict[tuple(value)][0] + supp_dict[tuple(value)][1]))


def main():
    global k
    ##    pos_filepath = sys.argv[1] # filepath to positive class file
    ##    neg_filepath = sys.argv[2] # filepath to negative class file
    ##    k = int(sys.argv[3])
    # TODO: read the dataset files and call your miner to print the top k itemsets
    # test constnats
    pos_filepath = 'positive.txt'
    neg_filepath = 'negative.txt'
    k = 1
    if __name__ == "__main__":
        sequence_mining(pos_filepath, neg_filepath, k)
        print_frequent(freq_dict, supp_dict)


main()
