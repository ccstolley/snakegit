#!/usr/bin/env python

import os
import os.path

import snakes.util

def main():
	"""docstring for main"""
	home = os.environ.get('SNAKEGIT_HOME', os.path.expanduser('~/.snakegit'))
	pwd = os.getcwd()
	os.chdir(home)
	snakes.util.run_cmd('git fetch && git pull')
  snakes.util.run_cmd("{0}/bin/python setup.py install".format(home))	
	snakes.util.run_cmd("{0}/bin/config".format(home))
	os.chdir(pwd)

if __name__ == '__main__':
	main()
