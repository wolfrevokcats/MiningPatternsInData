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

    # Support 1-length seq
    # print("--- Positive Dict ---")
    # print(dict_pos)
    # print("--- Negative Dict ---")
    # print(dict_neg)
    def get_support(list_of_tuples):
        counter = len(set([x[0] for x in list_of_tuples]))
        return counter

    def combine_list(state, dataset_pos, dataset_neg):
        comb = list(set().union(dataset_pos[state], dataset_neg[state]))
        return comb

    def prune_tx_pos_list(tx_pos_list, first_occurencies):
        pruned_tx_pos_list = []
        for tx, pos in tx_pos_list:
            # good position
            if tx in first_occurencies and first_occurencies[tx] < pos:
                pruned_tx_pos_list.append( (tx, pos) )

        return pruned_tx_pos_list

    def get_first(tx_pos_list):
        first_occurrencies = {}
        for tx, pos in tx_pos_list:
            if tx in first_occurrencies.keys():
                # update if already there
                first_occurrencies[tx] = min(first_occurrencies[tx], pos)
            else:
                # add new value
                first_occurrencies[tx] = pos

        return first_occurrencies

    def prune(dict_dataset, state):
        # get first occurrencies of state
        tx_pos_list = dict_dataset[state]

        first_occurrencies = get_first(tx_pos_list)

        # prune dataset using previous information
        pruned_dataset = {
            itemset: prune_tx_pos_list(tx_pos_list, first_occurrencies)
            for itemset, tx_pos_list in dict_dataset.items()
        }

        return pruned_dataset

    def dfs(state, results, dict1, dict2, k):
        # compute support for current state
        supp1 = get_support(dict1[state])
        supp2 = get_support(dict2[state])
        supp_tot = supp1 + supp2

        # no itemset transactions
        if supp_tot == 0:
            return

        if len(results.keys()) == k:
            if supp_tot < min(results.keys()):
                # uninteresting itemset
                return
            else:
                # remove the least interesting if our is better
                del results[min(results.keys())]

        if len(results.keys()) > k:
            # error state
            exit(1)

        # create empty container if necessary and add current state
        if supp_tot not in results.keys():
            results[supp_tot] = []

        results[supp_tot].append( (state, supp1, supp2) )

        # prune each dataset separately

        # get first occurencies for each transaction of state
        pruned_dataset1 = prune(dict1, state)
        pruned_dataset2 = prune(dict2, state)

        # join dictionary keys
        comb_items = set(pruned_dataset1.keys()).union(set(pruned_dataset2.keys()))

        for item in comb_items:
            if item != state:
                new_state = (*state, *item)

                print(pruned_dataset1)

                # create an entry in both datasets for new_state (separately)
                state_first_occurencies1 = get_first(dict1[state])
                state_first_occurencies2 = get_first(dict2[state])

                pruned_dataset1[new_state] = prune_tx_pos_list(pruned_dataset1[item],
                                                               state_first_occurencies1)

                pruned_dataset2[new_state] = prune_tx_pos_list(pruned_dataset2[item],
                                                               state_first_occurencies1)

                # merge current state with a new item and run again
                dfs(new_state, results, pruned_dataset1, pruned_dataset2, k)

    def spade(dataset_pos, dataset_neg, k):
        # convert keys to tuple
        dict_pos = {(key, ): value for key, value in dataset_pos.get_v().items()}
        dict_neg = {(key, ): value for key, value in dataset_neg.get_v().items()}

        # use single items from both datasets
        results = {}
        single_items = set(dict_pos.keys()).union(dict_neg.keys())
        for single_item in single_items:
            dfs(single_item, results, dict_pos, dict_neg, k)

        for supp_total, elements in results.items():
            for itemset, supp1, supp2 in elements:
                print(list(itemset), supp1, supp2, supp_total)

    # First call
    spade(dataset_pos, dataset_neg, k)

if __name__ == '__main__':
    # Possible tests:
    # prot1_PKA_group15.txt
    # prot2_SRC1521.txt
    # reu1_acq.txt
    # reu2_earn.txt

    # sequence_mining("reu1_acq.txt","reu2_earn.txt",600)

    # sequence_mining("prot1_PKA_group15.txt","prot2_SRC1521.txt",5)

    sequence_mining("positive.txt","negative.txt",7)
