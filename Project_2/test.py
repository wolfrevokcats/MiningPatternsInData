import itertools
from copy import deepcopy

k = {7: [('A','B'),('C','E')], 2: ('C','D')}
l = {7: ('Ck')}
print(k.items())
possible_children = [items for freq, items in k.items()]
print(possible_children)
possible_children = [i for i in list(itertools.chain.from_iterable(possible_children))]
print(possible_children)

print(deepcopy(k))
new_db = {r:v for r,v in k.items() if r in l}
print("new",new_db)