from frequent_itemset_miner import Dataset

list_dataset = ['mushroom.dat', 'chess.dat', 'retail.dat']

def get_size():
    for i in list_dataset:
    [data,T] = Dataset(i,0.8)
    return len(data.items())


