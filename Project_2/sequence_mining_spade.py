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

    def dfs(freq_dict, itemset, dataset_pos, dataset_neg, k):

        # compute supp itemset in dataset
        comb_support = get_support(dataset_pos[itemset],dataset_neg[itemset])
        print("Combinet support of item: ", itemset, " = ", comb_support)
        # save it in results:
        if comb_support in freq_dict:
            # comb_support is an existing key in freq_dict
            freq_dict[comb_support].append([itemset])
        else:
            # comb_support not in freq_dict
            # freq_dict is full
            if len(freq_dict.keys()) == k:
                # check the keys: if comb-supp < min freq
                if comb_support < min(freq_dict.keys()):
                    return
                else:
                    # remove the actual min freq
                    del freq_dict[min(freq_dict.keys())]
                    freq_dict[comb_support] = [itemset]
            # freq_dict is not full
            freq_dict[comb_support] = [itemset]
        # if comb in results:
            # append itemset nella lista
        # else:
            # if # chiavi in rsults == k
                # if comb < min freq
                    # return
                # else
                    # rimuovo la attuale chiave minima
                    # inserisco <chiave,itemset> in results: results[supp].append(itemset)
            # inserisco chiave in supps
            # inserisco itemset in lista di results: results[supp].append(itemset)

        # pruning

        # create dictionary for itemset: {<transaction,first occurrence of itemset in that transaction>}
        # prune_dataset = {}
        # togli prime occorrenze
        # togli i valori precedenti alle prime occ
        # for all other items in dataset.keys()
            #  for all tuple in items:
                # check in dict_first:
                # se il primo oggeto tupla in dict_first
                    # check se secondo oggetto della tupla > dict_fist[oggetto tupla]
                        # inserisco tupla in prune_dataset

        # items = lis(set(prune_dataset_1.keys()).union(set(prune_dataset_2.keys()))
        # come faccio a considerare entrambi i dataset insieme

        # for state in items with state != itemset
            # y = concatzione di state a itemset
            # combinare le liste di occurr tra state e itemset
                # check in dict_first:
                # se il primo oggeto tupla in dict_first
                # check se secondo oggetto della tupla > dict_fist[oggetto tupla]
                # inserisco tupla in prune_dataset

            # dfs(y,prune_dataset_1,prune_data_set_2)

    def spade(dataset_pos, dataset_neg, k):
        dict_pos = dataset_pos.get_v()
        dict_neg = dataset_neg.get_v()

        # 1) Create itemsets from single items
        valid_itemsets_pos = [k for k in dict_pos.keys()]
        valid_itemsets_neg = [j for j in dict_neg.keys()]
        itemsets = list(set(valid_itemsets_neg).union(set(valid_itemsets_pos)))

        # 2) Crea una list vuota results
        # results = {item: [supp_pos supp_neg supp_pos+supp_neg]}
        result = {}

        for item in itemsets.keys():
            dfs(result,[item],dataset_pos,dataset_neg)


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

