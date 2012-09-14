#!/usr/bin/env python

import argparse
import boto
from boto.s3.key import Key
from boto.s3.bucket import Bucket

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', type=str,
			help="The file to upload", required=True)
	parser.add_argument('-e', '--environment', type=str,
			help="The environment to upload into", required=True)
	parser.add_argument('-n', '--name', type=str,
			help="Name of the project", required=True)
	parser.add_argument('-b', '--bucket', type=str,
			help="Bucket to upload", required=True)

	args = parser.parse_args()

	conn = boto.connect_s3()
	bucket = Bucket(conn, args.bucket)
	key = Key(bucket)
	key.key = "{0}/{1}/{2}".format(args.name,
			args.environment,
			args.file)
	key.set_contents_from_filename(args.file)

if __name__ == "__main__":
	main()
