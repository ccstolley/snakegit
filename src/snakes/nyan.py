#!/usr/bin/env python

import snakes.util
import os.path

def main():
	"""docstring for main"""
	snakes.util.run_cmd("bash {0}".format(os.path.join(os.path.dirname(__file__), 
		'nyan')))

if __name__ == '__main__':
	main()
