import re
import sys


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

# Calculate the support
# We cna use this class to compute also the other supports, not just the 1-length
# Just be careful to pass a dictionary so just use {item we are considering,
# [list of tuples corresponding to its occurrence]}

# SEQUENCE MINING ALGORITHM


def sequence_mining(filepath1, filepath2, k):
    dataset_pos = Dataset(filepath1)
    dataset_neg = Dataset(filepath2)

    dict_pos = dataset_pos.get_v()
    dict_neg = dataset_neg.get_v()
    # Support 1-length seq
    # print("--- Positive Dict ---")
    # print(dict_pos)
    # print("--- Negative Dict ---")
    # print(dict_neg)



    def get_support(dict_symbol):
        t_id_set = set()
        dict_supp = {}
        for item in dict_symbol:
            # list of (t_id,t_pos_id)
            value = dict_symbol[item]
            for pair in value:
                t_id_set.add(pair[0])
                dict_supp[item] = len(t_id_set)

            t_id_set = set()

        return dict_supp

    supp_pos = get_support(dict_pos)
    supp_neg = get_support(dict_neg)

    # Create the first k-most frequent dictionary: freq_dict
    # update_freq_dict(total_supp,item,minFrequency)

    def initialize_freq_dict(supp_pos, supp_neg, k):
        freq_dict = {}
        freq_items = set()
        for item in supp_pos:
            if item in supp_neg:
                # combined supp already present in the freq_dict, not max length
                if supp_pos[item]+supp_neg[item] in freq_dict:
                    freq_dict[supp_pos[item] + supp_neg[item]].append(item)
                    freq_items.add(item)
                # max length reached
                elif len(freq_dict) == k:
                    min_key = min(freq_dict.keys())
                    if supp_pos[item]+supp_neg[item] > min_key:
                        del freq_dict[min_key]
                        freq_dict[supp_pos[item]+supp_neg[item]] = [item]
                        freq_items.add(item)
                # combined supp not present, not max length
                else:
                    freq_dict[supp_pos[item] + supp_neg[item]] = [item]
                    freq_items.add(item)

        return [freq_dict, list(freq_items)]

    # calling the initialize_freq_dict() method
    [freq_dict, freq_items] = initialize_freq_dict(supp_pos, supp_neg, k)
    # print("Print freq dict")
    # print(freq_dict)

    def print_k_most(freq_dict):
        # {<key,value> = <freq,[list of items with freq]>}
        # {<1,['A','B']>}
        print("--- k-most frequent dictionary ---")
        for freqs in freq_dict:
            for items in freq_dict[freqs]:
                print([items],freqs)

    # calling the print_k_most() method
    print_k_most(freq_dict)

    def update_freq_dict(freq_dict, total_supp, item, minFrequency):
        # combined supp already present in the freq_dict, not max length
        if total_supp in freq_dict:
            freq_dict[total_supp].append(item)
        # max length reached
        elif len(freq_dict) == minFrequency:
            min_key = min(freq_dict.keys())
            if total_supp > min_key:
                del freq_dict[min_key]
                freq_dict[total_supp] = [item]
        # combined supp not present, not max length
        else:
            freq_dict[total_supp] = [item]

    def dfs(state,dataset_pos,dataset_neg,freq_dict,freq_items,minFrequency):
        print("--- Entering DFS ----")
        # state should be the first element of the dictionary
        # state = list(dataset_pos.keys)[0]
        print("Considering item: ", state)
        # get all tuple not first occurrences
        D_state = {}
        y = 1
        occurr_pos = dataset_pos[state]
        occurr_neg = dataset_neg[state]

        for sub_items in dataset_pos[state]:
            print("sub_items = ",sub_items)
            print(sub_items[0])
            #t_id = sub_items[0][0]
            t_id = 1
            #if sub_items[y][0] == t_id:
                # same t_id
            #    D_state[state] = sub_items[y]
            #    y += 1

        print(D_state)
        # first transition: dataset = whole dictionary dataset_pos and dataset_neg
        valid_items = [k for k in freq_items]
        print("valid items")
        print(valid_items)




    def spade(d_pos, d_neg, supp_pos, supp_neg, minFrequency):

        for item, transactions in d_pos.items():
            if item in d_neg.keys():
                total_supp = supp_pos[item]+supp_neg[item]
                if total_supp >= minFrequency:
                    # print([item], supp_pos[item], supp_neg[item], total_supp)
                    # update the freq_dict
                    update_freq_dict(freq_dict, total_supp, item, minFrequency)

        dfs(list(d_pos.keys())[0], d_pos, d_neg, freq_dict, freq_items, minFrequency)

    #D, T = verticalRepresentation(dataset)
    #ECLAT(D, minFrequency, T)

    spade(dict_pos,dict_neg,supp_pos,supp_neg,k)

if __name__ == '__main__':
    # Possible tests:
    # prot1_PKA_group15.txt
    # prot2_SRC1521.txt
    # reu1_acq.txt
    # reu2_earn.txt

    # sequence_mining("reu1_acq.txt","reu2_earn.txt",600)

    # sequence_mining("prot1_PKA_group15.txt","prot2_SRC1521.txt",5)

    sequence_mining("positive.txt","negative.txt",7)

