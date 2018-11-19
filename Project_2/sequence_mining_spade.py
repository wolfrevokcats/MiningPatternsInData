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

    def get_support(list_1,list_2):
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

    def prune(itemset,dataset_pos):

        first_occurr_POS = get_first(itemset,dataset_pos)
        prune_dataset_POS = {itemset: list(set(dataset_pos[itemset]).difference(set(list(first_occurr_POS.items()))))}

        possible_candidates = [x for x in dataset_pos.keys() if x != itemset]
        # print("poss cand",possible_candidates)
        for other_items in possible_candidates:
            for values in dataset_pos[other_items]:
                trans, pos = values
                if trans in first_occurr_POS:
                    # if the trans is present: other_items comes after itemset
                    if pos > first_occurr_POS[trans]:
                        # print("This occ ", (trans, first_occurr_POS[trans]), "before this", (trans, pos))
                        if other_items not in prune_dataset_POS:
                            prune_dataset_POS[other_items] = [(trans, pos)]
                        else:
                            prune_dataset_POS[other_items].append((trans, pos))

        return prune_dataset_POS

    def dfs(freq_dict, itemset, dataset_pos, dataset_neg, k):

        # compute combined occurences: list of tuple

        combined_occurr = list(set(dataset_pos[itemset]).union(set(dataset_neg[itemset])))
        # print("Combined occurrences of item: ", itemset)
        # print(combined_occurr)
        # comb_support = get_support(dataset_pos[itemset],dataset_neg[itemset])
        combined_support = len(combined_occurr)
        # print("Combined support of item: ", itemset, " = ", combined_support)
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
            freq_dict[combined_support] = [itemset]

        # Pruning
        # print(" ---- Creating Projected Database of item ", itemset, "----")

        # create dictionary for itemset: {<transaction,first occurrence of itemset in that transaction>

        prune_dataset_pos = prune(itemset,dataset_pos)
        prune_dataset_neg = prune(itemset,dataset_neg)
        #print(prune_dataset_pos)
        #print(prune_dataset_neg)

        # print(freq_dict)

        items = list(set(prune_dataset_pos.keys()).union(set(prune_dataset_pos.keys())))
        #print(items)
        for entry in items:
            dfs(freq_dict,entry,prune_dataset_pos,prune_dataset_neg,k)


    def spade(dataset_pos, dataset_neg, k):
        dict_pos = dataset_pos.get_v()
        dict_neg = dataset_neg.get_v()

        # 1) Create itemsets from single items
        valid_itemsets_pos = [k for k in dict_pos.keys()]
        valid_itemsets_neg = [j for j in dict_neg.keys()]
        itemsets = list(set(valid_itemsets_neg).intersection(set(valid_itemsets_pos)))
        print(itemsets)

        # 2) Compute supports
        supp_pos = get_first_support(dict_pos)
        supp_neg = get_first_support(dict_neg)
        print(supp_neg)
        print(supp_pos)

        # 2) Crea una list vuota results
        combined_support = {}
        freq_dict = {}
        for item in itemsets:
            combined_support[item] = [supp_pos[item], supp_neg[item], supp_pos[item] + supp_neg[item]]
        print(combined_support)

        # 3) Update of the frequent dictionary
        for item in itemsets:
            update_freq_dict(freq_dict, combined_support[item], item, k)

        print(freq_dict)


        # 4) Extract k-most frequent items
        k_most = []
        for key in freq_dict:
            if len(freq_dict[key]) != 1:
                for elements in range(len(freq_dict[key])):
                    k_most.append(freq_dict[key][elements][0])
            else:
                k_most.append(freq_dict[key][0][0])

        print(k_most)

        # 5) DFS on k-most frequent items
        for i in k_most:
            dfs(freq_dict, i, dict_pos, dict_neg, k)

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

