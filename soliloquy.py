#!/usr/bin/python

import csv
from datetime import date, datetime
import random
import os
import glob
from pathlib import Path
import argparse

class cmdTags:
	BLUE = "\033[94m"
	BOLD = "\033[1m"
	END  = "\033[0m"
pass

def printRow(row, dateFmt):
	if len(dateFmt) > 0:
		print("\r" + "Today is " + cmdTags.BLUE + dt.strftime(dateFmt) + cmdTags.END)
	pass

	print("Word of the day: " + cmdTags.BOLD + row[0] + cmdTags.END + " (" + row[1] + ") — " + row[2])
	print()
pass

# Get todays timestamp
dt = datetime.combine(date.today(), datetime.min.time())
timestamp = round(datetime.timestamp(dt))

# Parse arguments
parser = argparse.ArgumentParser(description="Print a word of the day")
parser.add_argument("-n", dest="cache", action="store_const", const=False, default=True, help="Dont' use cache")
parser.add_argument("-d", dest="dateFmt", default="%A, %B %-d", help="Specify date format")
args = parser.parse_args()

# Print
li = []
cache = Path("/tmp/wod-cache-" + str(timestamp))
if (args.cache and cache.is_file()):
	# Print string from cache
	with open(cache, "r") as csvfile:
		printRow(list(csv.reader(csvfile, delimiter="|"))[0], args.dateFmt)
	pass
else:
	# Read and merge all csv files
	for filename in glob.glob(os.path.dirname(os.path.realpath(__file__)) + "/dictionary/*.csv"):
		with open(filename) as csvfile:
			readerL = list(csv.reader(csvfile, delimiter="|"))
			li += readerL
		pass
	pass

	# Print random string
	random.seed(timestamp)
	chosenRow = random.choice(li)
	printRow(chosenRow, args.dateFmt)

	# Write cache
	if (args.cache):
		csv.writer(open(cache, "w"), delimiter="|", lineterminator="\n").writerow(chosenRow)
	pass
pass
