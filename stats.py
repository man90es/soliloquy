#!/usr/bin/python

import csv
import os
import glob

# Read and merge all csv files
path = os.path.dirname(os.path.realpath(__file__)) + "/dictionary/*.csv"
li = []

for filename in glob.glob(path):
	with open(filename) as csvfile:
		readerL = list(csv.reader(csvfile, delimiter="|"))
		li += readerL

# Print the number of rows
print(str(len(li)) + "\033[0m")
