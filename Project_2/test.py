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


"""l = ('A','B','C')
k = list(l)
j = tuple(k[:2]+k[2:])
print(j)"""


superpattern = ('A',)
pattern = ('B',)
def is_subpattern(superpattern,pattern):
    sub_pattern = list(superpattern)
    pattern = list(pattern)
    print(pattern)
    print(sub_pattern)
    sub_len = len(sub_pattern)
    leng = len(pattern)
    i = 0
    while i < sub_len:
        print("start")
        print("it = ",i)
        if pattern[i] != sub_pattern[i]:
            print("mismatch: ", pattern[i],"vs",sub_pattern[i])
            pattern.remove(pattern[i])
            print("pattern = ",pattern)
            #i -= 1
            #print("decrementing i = ", i)
            if len(pattern) < sub_len:
                return False
        else:
            if len(pattern) == sub_len:
                return False
            print("match: ", pattern[i], "=", sub_pattern[i])
            i += 1
            print("it = ", i)
            print("end")
    return True
print("value", is_subpattern(pattern,superpattern))
