#!/usr/bin/python

import csv
import os
import glob

li = []

# Read and merge all csv files
for filename in glob.glob(os.path.dirname(os.path.realpath(__file__)) + "/dictionary/*.csv"):
	with open(filename) as csvfile:
		readerL = list(csv.reader(csvfile, delimiter="|"))
		li += readerL
	pass
pass

# Print the number of rows
print(str(len(li)) + "\033[0m")
