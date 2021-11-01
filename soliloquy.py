#!/usr/bin/python

from flask import Flask
import csv
from datetime import date, datetime
import random
import os
import glob
from pathlib import Path
import argparse


# Init Flask
app = Flask(__name__)


def get_timestamp():
	dt = datetime.combine(date.today(), datetime.min.time())
	return round(datetime.timestamp(dt))


def parse_args():
	parser = argparse.ArgumentParser(description="Soliloquy server")

	parser.add_argument(
		"-n", dest="n", action="store_const",
		const=True, default=False, help="Dont' use cache"
	)

	return parser.parse_args()


@app.route("/", methods=["GET"])
def get_root():
	timestamp = get_timestamp()
	cache = Path("/tmp/wod-cache-" + str(timestamp))
	use_cache = not args.n and cache.is_file()

	# Print string from cache if it's allowed and exists
	if (use_cache):
		with open(cache, "r") as csvfile:
			response = csvfile.readline()

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
		response = "|".join(random.choice(li)) + "\n"

		# Write cache
		if (not args.n):
			with open(cache, "w") as csvfile:
				csvfile.write(response)

	return app.response_class(
		response=response,
		status=200,
		mimetype="text/plain"
	)


if __name__ == "__main__":
	args = parse_args()
	app.run()
