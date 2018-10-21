import numpy as np
import csv
import pandas as pd
from mlxtend.frequent_patterns import apriori


# dataset = np.loadtxt('toy.dat')
#data2 = open('toy.dat','rb')
# array = np.genfromtxt('toy.dat',delimiter=' ')
# arrays = [np.array(map(int, line.split())) for line in open('toy.txt')]


# df = pd.read_table('mushroom.dat')
# df.to_excel('mushroom.xlsx')

"""
Skeleton file for the project 1 of the LINGI2364 course.
Use this as your submission file. Every piece of code that is used in your program should be put inside this file.

This file given to you as a skeleton for your implementation of the Apriori and Depth
First Search algorithms. You are not obligated to use them and are free to write any class or method as long as the
following requirements are respected:

Your apriori and alternativeMiner methods must take as parameters a string corresponding to the path to a valid
dataset file and a double corresponding to the minimum frequency.
You must write on the standard output (use the print() method) all the itemsets that are frequent in the dataset file
according to the minimum frequency given. Each itemset has to be printed on one line following the format:
[<item 1>, <item 2>, ... <item k>] (<frequency>).
Tip: you can use Arrays.toString(int[] a) to print an itemset.

The items in an itemset must be printed in lexicographical order. However, the itemsets themselves can be printed in
any order.

Do not change the signature of the apriori and alternative_miner methods as they will be called by the test script.

__authors__ = "<write here your group, first name(s) and last name(s)>"
"""


class Dataset:
	"""Utility class to manage a dataset stored in a external file."""

	def __init__(self, filepath):
		"""reads the dataset file and initializes files"""
		self.transactions = list()
		self.items = set()

		try:
			lines = [line.strip() for line in open(filepath, "r")]
			lines = [line for line in lines if line]  # Skipping blank lines
			for line in lines:
				transaction = list(map(int, line.split(" ")))
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


def apriori(filepath, minFrequency):
	"""Runs the apriori algorithm on the specified file with the given minimum frequency"""
	# TODO: implementation of the apriori algorithm
	print("Not implemented")


def alternative_miner(filepath, minFrequency):
	"""Runs the alternative frequent itemset mining algorithm on the specified file with the given minimum frequency"""
	# TODO: either second implementation of the apriori algorithm or implementation of the depth first search algorithm
	dataset = Dataset(filepath)



	print("Not implemented")

# data = Dataset('toy.dat')
# items = data.items
# items_num = data.items_num()
# trans = data.transactions
# trans_num = data.trans_num()

# print('Itemset: ', items)
# print('Number of items: ', items_num)
# print('Transactions: ', trans)
# print('Number of transactions: ', trans_num)


