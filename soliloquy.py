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
	END =  "\033[0m"


def print_row(row, dateFmt):
	if len(dateFmt) > 0:
		date_str = cmdTags.BLUE + date.today().strftime(dateFmt) + cmdTags.END
		print("\r" + "Today is", date_str)
	pass

	word = cmdTags.BOLD + row[0] + cmdTags.END
	pos = "(" + row[1] + ")"
	definition = row[2]
	print("Word of the day:", word, pos, "—", definition, "\n")


def get_timestamp():
	dt = datetime.combine(date.today(), datetime.min.time())
	return round(datetime.timestamp(dt))


def parse_args():
	parser = argparse.ArgumentParser(description="Print a word of the day")

	parser.add_argument(
		"-n", dest="n", action="store_const",
		const=True, default=False, help="Dont' use cache"
	)
	parser.add_argument(
		"-d", dest="d",
		default="%A, %B %-d", help="Specify date format"
	)

	return parser.parse_args()


if __name__ == "__main__":
	timestamp = get_timestamp()
	args = parse_args()
	cache = Path("/tmp/wod-cache-" + str(timestamp))
	use_cache = not args.n and cache.is_file()

	# Print string from cache if it's allowed and exists
	if (use_cache):
		with open(cache, "r") as csvfile:
			print_row(list(csv.reader(csvfile, delimiter="|"))[0], args.d)

	# Generate a string
	else:
		# Read and merge all csv files
		path = os.path.dirname(os.path.realpath(__file__)) + "/dictionary/*.csv"
		li = []

		for filename in glob.glob(path):
			with open(filename) as csvfile:
				readerL = list(csv.reader(csvfile, delimiter="|"))
				li += readerL

		# Print a random string
		random.seed(timestamp)
		chosenRow = random.choice(li)
		print_row(chosenRow, args.d)

		# Write cache
		if (not args.n):
			writer = csv.writer(open(cache, "w"), delimiter="|", lineterminator="\n")
			writer.writerow(chosenRow)
