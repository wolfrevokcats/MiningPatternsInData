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

# SEQUENCE MINING ALGORITHM
def sequence_mining(filepath1, filepath2, k):
    dataset_pos = Dataset(filepath1)
    dataset_neg = Dataset(filepath2)

    def get_support(list_1, list_2):
        counter = len(set([x[0] for x in list_1]).union([x[0] for x in list_2]))
        return counter

    def get_first_support(dict_symbol):
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


    def get_first(itemset,dataset):

        first_occurr = {}
        for iter in range(len(dataset[itemset])):
            key = dataset[itemset][iter][0]
            if key not in first_occurr :
                # transaction not present
                first_occurr[key] = dataset[itemset][iter][1]
            else:
                # transaction is present
                # updating the position
                if dataset[itemset][iter][1] < first_occurr[key]:
                    first_occurr[key] = dataset[itemset][iter][1]

        return first_occurr

    def update_freq_dict(freq_dict, list_supp, item, k):
        # combined supp already present in the freq_dict, not max length
        total_supp = list_supp[2]
        if total_supp in freq_dict:
            freq_dict[total_supp].append([item, list_supp[0],list_supp[1]])
        # max length reached
        elif len(freq_dict) == k:
            min_freq = min(freq_dict.keys())
            if total_supp > min_freq:
                del freq_dict[min_freq]
                freq_dict[total_supp] = [item, list_supp[0], list_supp[1]]
        # combined supp not present, not max length
        else:
            freq_dict[total_supp] = [[item, list_supp[0], list_supp[1]]]

    def prune(freq_dict, itemset, dataset_pos, dataset_neg, k_most):

        # first occurrences
        print("First occurrences of", itemset)
        first_occurr_pos = get_first(itemset, dataset_pos)
        print(first_occurr_pos)
        # insert every not-first occurrences in the prune-dataset
        #print("Inserting in prune_dataset the not-first occurrences of item", itemset)
        prune_dataset_pos = {str(itemset+itemset): list(set(dataset_pos[itemset]).difference(set(list(first_occurr_pos.items()))))}
        #print(prune_dataset)
        possible_candidates_pos = [x for x in k_most if x != itemset]
        # print("poss cand",possible_candidates)

        for other_items in possible_candidates_pos:
            print("Considering item", other_items, "in k-most database")
            for values in dataset_pos[other_items]:
                trans, pos = values
                if trans in first_occurr_pos:
                    # if the trans is present: other_items comes after itemset
                    if pos > first_occurr_pos[trans]:
                        # print("This occ ", (trans, first_occurr_POS[trans]), "before this", (trans, pos))
                        if other_items not in prune_dataset_pos:
                            prune_dataset_pos[str(itemset+other_items)] = [(trans, pos)]
                        else:
                            prune_dataset_pos[str(itemset+other_items)].append((trans, pos))

            # update del freq_dict
            update_freq_dict(freq_dict, dataset_pos[other_items], dataset_neg[other_items], other_items, k)

        # first occurrences
        print("First occurrences of", itemset)
        first_occurr_neg = get_first(itemset, dataset_neg)
        print(first_occurr_neg)
        # insert every not-first occurrences in the prune-dataset
        # print("Inserting in prune_dataset the not-first occurrences of item", itemset)
        prune_dataset_neg = {str(itemset + itemset): list(set(dataset_neg[itemset]).difference(set(list(first_occurr_neg.items()))))}
        # print(prune_dataset)
        possible_candidates_neg = [x for x in k_most if x != itemset]
        # print("poss cand",possible_candidates)

        for other_items in possible_candidates_neg:
            print("Considering item", other_items, "in k-most database")
            for values in dataset_neg[other_items]:
                trans, pos = values
                if trans in first_occurr_neg:
                # if the trans is present: other_items comes after itemset
                    if pos > first_occurr_neg[trans]:
                    # print("This occ ", (trans, first_occurr_POS[trans]), "before this", (trans, pos))
                        if other_items not in prune_dataset_neg:
                            prune_dataset_neg[str(itemset + other_items)] = [(trans, pos)]
                        else:
                            prune_dataset_neg[str(itemset + other_items)].append((trans, pos))

            # update del freq_dict
            update_freq_dict(freq_dict, dataset_neg[other_items], dataset_pos[other_items], other_items, k)

        return [prune_dataset_pos, prune_dataset_neg]

    def update_results(freq_dict, kmost, results, itemset):
        y = 0
        found = False
        for keys, values in freq_dict.items():
            y=0
            for val in values:
                if val[0] == itemset:
                    results.append([itemset, freq_dict[keys][y][1], freq_dict[keys][y][2], keys])
                    del_key = keys
                    del_pos = y
                    found = True
                    break
                else:
                    y += 1
            if found:
                break

        del freq_dict[del_key][del_pos]
        return results

    def dfs(freq_dict, results, kmost, itemset, dataset_pos, dataset_neg, k):

        # compute combined occurences: list of tuple
        results = update_results(freq_dict, kmost, results, itemset)
        print("Results")
        print(results)

        """combined_occurr = list(set(dataset_pos[itemset]).union(set(dataset_neg[itemset])))
        combined_support = len(combined_occurr)
        # save it in results:
        if combined_support in freq_dict:
            # comb_support is an existing key in freq_dict
            freq_dict[combined_support].append([itemset])
        else:
            # comb_support not in freq_dict
            # freq_dict is full
            if len(freq_dict.keys()) == k:
                # check the keys: if comb-supp < min freq
                if combined_support < min(freq_dict.keys()):
                    return
                else:
                    # remove the actual min freq
                    del freq_dict[min(freq_dict.keys())]
                    freq_dict[combined_support] = [itemset]
            # freq_dict is not full
            freq_dict[combined_support] = [itemset]"""

        [prune_dataset_pos, prune_dataset_neg] = prune(freq_dict, dataset_pos, dataset_neg, itemset, kmost)
        print("Pruned POS dataset of item", itemset)
        print(prune_dataset_pos)
        print("Pruned NEG dataset of item", itemset)
        print(prune_dataset_neg)

        # print(freq_dict)

        items = list(set(prune_dataset_pos.keys()).union(set(prune_dataset_pos.keys())))
        #print(items)
        # for entry in items:
        if not kmost:
            dfs(freq_dict,kmost,prune_dataset_pos,prune_dataset_neg,k)


    def spade(dataset_pos, dataset_neg, k):
        dict_pos = dataset_pos.get_v()
        dict_neg = dataset_neg.get_v()

        # 1) Create itemsets from single items
        valid_itemsets_pos = [k for k in dict_pos.keys()]
        valid_itemsets_neg = [j for j in dict_neg.keys()]
        itemsets = list(set(valid_itemsets_neg).intersection(set(valid_itemsets_pos)))
        print("Items present in both dataset")
        print(itemsets)

        # 2) Compute supports
        supp_pos = get_first_support(dict_pos)
        supp_neg = get_first_support(dict_neg)
        print("Dict of support for positive dataset")
        print(supp_pos)
        print("Dict of support for negative dataset")
        print(supp_neg)

        # 2) Crea una list vuota results
        combined_support = {}
        freq_dict = {}
        for item in itemsets:
            combined_support[item] = [supp_pos[item], supp_neg[item], supp_pos[item] + supp_neg[item]]

        print("Dict of combined support [pos+neg]")
        print(combined_support)

        # 3) Update of the frequent dictionary
        for item in itemsets:
            update_freq_dict(freq_dict, combined_support[item], item, k)
        print("Dict of frequent itemse")
        print(freq_dict)


        # 4) Extract k-most frequent items
        k_most = []
        for key in freq_dict:
            if len(freq_dict[key]) != 1:
                for elements in range(len(freq_dict[key])):
                    k_most.append(freq_dict[key][elements][0])
            else:
                k_most.append(freq_dict[key][0][0])
        print("K-most frequent items")
        print(k_most)

        # 5) DFS on k-most frequent items
        results = []
        for i in k_most:
            dfs(freq_dict, results, k_most, i, dict_pos, dict_neg, k)

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

    sequence_mining("positive.txt","negative.txt",6)

