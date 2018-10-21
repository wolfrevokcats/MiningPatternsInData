import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

#datasets = ['chess.dat', 'mushroom.dat', 'retail.dat', 'connect.dat', 'pumsb.dat']
datasets = ['chess.dat', 'mushroom.dat', 'retail.dat', 'connect.dat']
# y axis
time_list = []
time_error = []
# x axis
size_list = []

for i in datasets:
    df = pd.read_csv('time_test_' + i, sep=' ', header=None, names = ["run", "time"])
    time = np.array(df["time"])
    ci = 1.645*np.std(time)/np.sqrt(len(time))
    time_list.append(np.mean(time))
    time_error.append(ci)
    with open("../"+ i, "rb") as infile:
        # print(os.path.getsize(infile.name))
        size_list.append(os.path.getsize(infile.name)/1e3)

# print(time_list)
# print(time_error)
# print(size_list)






plt.figure()
plt.errorbar(size_list, time_list, yerr=time_error)
plt.title("Time vs Dataset size")
plt.xlabel("Dataset size [Kbyte]")
plt.ylabel("Time [s]")
plt.yscale("log")
plt.grid()
plt.tight_layout()
plt.savefig('time_vs_size.pdf')

plt.show()