import itertools
from copy import deepcopy

k = {1: ('A','B'), 2: ('C','D')}
l = {7: ('A')}
print(k)
possible_children = [items for freq, items in k.items()]
print(possible_children)
possible_children = [i[-1] for i in list(itertools.chain.from_iterable(possible_children))]
print(possible_children)

print(deepcopy(k))
new_db = {r:v for r,v in k.items() if r in k}
print("new",new_db)