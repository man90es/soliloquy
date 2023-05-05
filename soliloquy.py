#!env python

from datetime import date, datetime
from flask import Flask, request
from pathlib import Path
import argparse
import csv
import glob
import json
import os
import random
import sys


# Init Flask
app = Flask(__name__)
pwd = os.path.dirname(os.path.realpath(__file__))
dictionary_files = glob.glob(pwd + "/dictionary/*.csv")

if (1 > len(dictionary_files)):
	sys.exit("Can't find dictionary csv files in the \"dictionary\" catalogue!")


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


def jsonify_row(row):
	d = {}

	i = row[0].index("/")
	d["word"] = row[0][0:i - 1]
	d["transcription"] = row[0][i:len(row[0])]
	d["partOfSpeech"] = row[1]
	d["meaning"] = row[2]

	return json.dumps(d)


@app.route("/", methods=["GET"])
def get_root():
	timestamp = request.args.get("ts", default=get_timestamp(), type=int)
	cache = Path("/tmp/wod-cache-" + str(timestamp))
	use_cache = not args.n and cache.is_file()

	# Print string from cache if it's allowed and exists
	if (use_cache):
		with open(cache, "r") as csvfile:
			response = list(csv.reader(csvfile, delimiter="|"))[0]
			csv_response = "|".join(response) + "\n"

	# Generate a string
	else:
		# Read and merge all csv files
		li = []

		for filename in dictionary_files:
			with open(filename) as csvfile:
				readerL = list(csv.reader(csvfile, delimiter="|"))
				li += readerL

		# Print a random string
		random.seed(timestamp)
		response = random.choice(li)
		csv_response = "|".join(response) + "\n"

		# Write cache
		if (not args.n and not cache.is_file()):
			with open(cache, "w") as csvfile:
				csvfile.write(csv_response)

	mime = request.headers["Accept"]

	if "*/*" in mime or "application/json" in mime:
		return app.response_class(
			response=jsonify_row(response),
			status=200,
			mimetype="application/json"
		)
	if "text/plain" in mime:
		return app.response_class(
			response=csv_response,
			status=200,
			mimetype="text/plain"
		)
	else:
		return app.response_class(
			status=412
		)


if __name__ == "__main__":
	args = parse_args()
	app.run()
