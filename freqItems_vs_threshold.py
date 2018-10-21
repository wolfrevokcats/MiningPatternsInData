import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

#datasets = ['chess.dat', 'mushroom.dat', 'retail.dat', 'connect.dat', 'pumsb.dat']
datasets = ['mushroom.dat','chess.dat']
# y axis
num_items_mushroom = []
num_items_chess = []

# mushroom: 0.125, chess: 0.5


thresholds_mushroom = np.linspace(0.125, 1, num=20)
for i in thresholds_mushroom:
    df = pd.read_csv('frequentItem_0.125_mushroom.dat', sep=']', header=None, names=["transaction", "frequency"])
    frequency = []
    frequency.append([float(freq[2:-1]) for freq in df["frequency"]])
    frequency = np.array(frequency)
    num_items_single = np.count_nonzero(frequency >= i)
    num_items_mushroom.append(num_items_single)

thresholds_chess = np.linspace(0.5, 1, num=10)
for i in thresholds_chess:
    df = pd.read_csv('frequentItem_0.5_chess.dat', sep=']', header=None, names=["transaction", "frequency"])
    frequency = []
    frequency.append([float(freq[2:-1]) for freq in df["frequency"]])
    frequency = np.array(frequency)
    num_items_single = np.count_nonzero(frequency >= i)
    num_items_chess.append(num_items_single)



plt.figure()
plt.plot(thresholds_mushroom, num_items_mushroom, label="mushroom.dat")
plt.plot(thresholds_chess, num_items_chess, label="chess.dat")
plt.title("Frequent items vs frequency")
plt.xlabel("Frequency ")
plt.ylabel("Number of frequent items")
plt.grid()
plt.tight_layout()
plt.legend()
plt.savefig('num_items_vs_threshold.pdf')

plt.show()