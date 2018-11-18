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

    def prune(itemset,dataset_pos):

        first_occurr_POS = get_first(itemset,dataset_pos)
        prune_dataset_POS = {itemset: list(set(dataset_pos[itemset]).difference(set(list(first_occurr_POS.items()))))}
        possible_candidates = [x for x in dataset_pos.keys() if x != itemset]
        print("poss cand",possible_candidates)
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

        print('here',prune_dataset_POS)

        prune_dataset = {}
        '''for keys in prune_dataset_POS.keys():
            newState = (*keys, itemset)
            newValue = prune_dataset_POS[keys]
            prune_dataset[newState] = newValue'''

        return prune_dataset_POS

    def dfs(freq_dict, itemset, dataset_pos, dataset_neg, k):

        # compute combined occurences: list of tuple
        try:
            combined_occurr = list(set(dataset_pos[itemset]).union(set(dataset_neg[itemset])))
        except:
            if itemset in dataset_pos[itemset]:
                combined_occurr = dataset_pos[itemset]
            else:
                combined_occurr = dataset_neg[itemset]
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
        print(" ---- Creating Projected Database of item ", itemset, "----")

        # create dictionary for itemset: {<transaction,first occurrence of itemset in that transaction>

        prune_dataset_pos = prune(itemset,dataset_pos)
        prune_dataset_neg = prune(itemset,dataset_neg)
        print(prune_dataset_pos)
        print(prune_dataset_neg)


        items = list(set(prune_dataset_pos.keys()).union(set(prune_dataset_pos.keys())))
        print(items)
        for entry in items:
            dfs(freq_dict,entry,prune_dataset_pos,prune_dataset_neg,k)

    def spade(dataset_pos, dataset_neg, k):
        dict_pos = dataset_pos.get_v()
        dict_neg = dataset_neg.get_v()

        # 1) Create itemsets from single items
        valid_itemsets_pos = [k for k in dict_pos.keys()]
        valid_itemsets_neg = [j for j in dict_neg.keys()]
        itemsets = list(set(valid_itemsets_neg).union(set(valid_itemsets_pos)))

        # 2) Crea una list vuota results
        # results = {item: [supp_pos supp_neg supp_pos+supp_neg]}
        freq_dict = {}

        for item in itemsets:
            dfs(freq_dict, item, dict_pos, dict_neg, k)


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
    sequence_mining("positive.txt","negative.txt",2)

