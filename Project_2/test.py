from sortedcontainers import SortedDict
import itertools


"""supp_dict = {('A',):(3,3),('C',):(1,2),('A','C',):(4,5)}
pc_contuple = [('A',),('C',)]
val = []
keys = {}
for i in pc_contuple:
    total_supp = supp_dict[i][0]+supp_dict[i][1]
    val.append(total_supp)
    keys[i] = total_supp

print('val',val)
print('ll',keys)

sorted_keys = list(keys.keys())
print(sorted_keys)

flip_dic = [k for k in sorted_keys]
flip_dic = [i[-1] for i in list(itertools.chain.from_iterable(flip_dic))]
print(flip_dic)"""


k = {('A','B',):(3,3)}
l = ('A','B','C')

