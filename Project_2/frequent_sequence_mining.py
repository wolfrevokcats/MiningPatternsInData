import re


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

def sequence_mining(filepath1,filepath2,k):
    dataset_pos = Dataset(filepath1)
    dataset_neg = Dataset(filepath2)

    dict_pos = dataset_pos.get_v()
    dict_neg = dataset_neg.get_v()
    # Support 1-length seq
    supp_pos = get_support(dict_pos)
    supp_neg = get_support(dict_neg)

    # Create the first k-most frequent dictionary: freq_dict
    def update_freq_dict(supp_pos,supp_neg,k):
        freq_dict = {}
        for item in supp_pos:
            if item in supp_neg:
                # combined supp already present in the freq_dict, not max length
                if supp_pos[item]+supp_neg[item] in freq_dict:
                    freq_dict[supp_pos[item] + supp_neg[item]].append(item)
                # max length reached
                elif len(freq_dict) == k:
                    min_key = min(freq_dict.keys())
                    if supp_pos[item]+supp_neg[item] > min_key:
                        del freq_dict[min_key]
                        freq_dict[supp_pos[item]+supp_neg[item]] = [item]
                # combined supp not present, not max length
                else:
                    freq_dict[supp_pos[item] + supp_neg[item]] = [item]

        return freq_dict

    # calling the initialize_freq_dict() method
    freq_dict = update_freq_dict(supp_pos, supp_neg, k)

    def print_k_most(freq_dict):
        # {<key,value> = <freq,[list of items with freq]>}
        # {<1,['A','B']>}
        print("--- k-most frequent dictionary ---")
        for freqs in freq_dict:
            for items in freq_dict[freqs]:
                print([items],freqs)

    # calling the print_k_most() method
    print_k_most(freq_dict)


    def SPADE(D_pos,D_neg,supp_pos,supp_neg,minFrequency):
    #    # minFrequency == k
    #    theta = minFrequency * T
        for item, transactions in D_pos.items():
            if item in D_neg.keys():
                total_supp = supp_pos[item]+supp_neg[item]
                if total_supp >= minFrequency:
                    print([item], supp_pos[item], supp_neg[item], total_supp)
                    # update the freq_dict
                    #update_freq_dict(total_supp,item,minFrequency)

    #    printFrequent([0], D, theta, T)

    #D, T = verticalRepresentation(dataset)
    #ECLAT(D, minFrequency, T)

    SPADE(dict_pos,dict_neg,supp_pos,supp_neg,k)

if __name__ == '__main__':
    # Possible tests:
    # prot1_PKA_group15.txt
    # prot2_SRC1521.txt
    # reu1_acq.txt
    # reu2_earn.txt

    # sequence_mining("reu1_acq.txt","reu2_earn.txt",600)

    # sequence_mining("prot1_PKA_group15.txt","prot2_SRC1521.txt",5)

    sequence_mining("positive.txt","negative.txt",7)
