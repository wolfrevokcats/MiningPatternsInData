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
	pass


def alternative_miner(filepath, minFrequency):
	"""Runs the alternative frequent itemset mining algorithm on the specified file with the given minimum frequency"""
	dataset = Dataset(filepath)

	def verticalRepresentation(dataset):
		"""Fill the dictionary with the iterations of the dataset"""
		D = dict(list(enumerate(dataset.transactions, 1)))
		# print('Dictionary: ', D)
		""" VERTICAL REPRESENTATION: Transform the database """
		# create supports list
		# create list of transactions
		list_items = list(dataset.items)
		list_trans = list(dataset.transactions)
		T = len(list_trans)
		"""Vertical Representation"""
		# create an empty list with length == number of items
		newD = {}
		for i in D:  # run through all trans in dict
			# print(i)
			for j in D[i]:  # run through the items in esch trans
				if j not in newD:
					newD[j] = [i]
				else:
					newD[j].append(i)
		y = 0
		support, frequency = [], []
		for i in list_items:
			support.append(len(newD[i]))
			frequency.append(support[y] / T)
			y = y + 1

		return newD, T


	def printFrequent(state, D, theta, T):
		valid_keys = [k for k in D.keys() if k > state[-1]]
		for j in valid_keys:
			new_state = [*state, j]

			# build projection D|state, j = D|new_state
			Dj = {}
			for k in valid_keys:
				if k > j:
					candidate = list(set(D[k]) & set(D[j]))
					if len(candidate) >= theta:
						Dj[k] = candidate

			for item, transactions in Dj.items():
				print([*new_state, item][1:], (len(Dj[item])) / T)

			# proceed to children
			printFrequent(new_state, Dj, theta, T)

	def ECLAT(D, minFrequency, T):
		theta = minFrequency*T
		for item, transactions in D.items():
			if len(transactions) >= theta:
				print([item], len(transactions) / T)
		printFrequent([0], D, theta, T)

	D, T = verticalRepresentation(dataset)
	ECLAT(D, minFrequency, T)

	print("Implemented")

if __name__ == "__main__":
	# dataset = Dataset('accidents.dat')
	# apriori('toy.dat', 1/8)
	alternative_miner('chess.dat', 0.5)

