# Importing the libraries
import numpy as np
import collections
from numpy import *


class DataSet:
    def __init__(self):
        """"Initialize the database obj: nrow == #rows, ncol == #ncols"""
        #self.nrow = nrow
        #self.ncol = ncol

    def loadDataSet(self):
        return [['B'],['E'],['AC'],['AE'],['BC'],['DE'],['CDE'],['ABC'],['ABE'],['ABCE']]

    # def shape(self):
        #return [self.nrow,self.ncol]


# print dataset
dataSet = DataSet()
print(dataSet.loadDataSet())
collections.Counter(dataSet)
# implementing sorting of itemsets





# minsup == 2
minsup = 2

#


