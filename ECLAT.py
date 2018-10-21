from frequent_itemset_miner import Dataset

class ECLAT:
    """Utility class to manage a dataset stored in a external file."""
    def eclat(filepath, minFrequency):
        """Returns the transaction at index i as an int array"""
        dataset = Dataset(filepath)
        D = dict(list(enumerate(dataset.transactions),1))
        print(D)
        list_items = list(dataset.items)
        list_trans = list(dataset.transactions)
        for i in list_items:
            for t in list_trans:
                if t.count(i) == 1:
                    print(i,'ok')

    eclat('toy.dat',2)




