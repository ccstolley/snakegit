#!/usr/bin/env python

import snakes.util
import os

def main():
	"""docstring for main"""
	if 'VIRTUALENV_HOME' in os.environ:
		venv = os.environ['VIRTUALENV_HOME']
	else:
		venv = 'vendor/python'
	if 'VENV_CACHE_HOME' in os.environ:
		cache = os.environ['VENV_CACHE_HOME']
	else:
		cache = 'vendor/cache'
	cmd = '{0}/bin/pip install --find-links=file://{1} --no-index --index-url=file:///dev/null --no-deps -r requirements.txt'.format(venv, cache)
	snakes.util.run_cmd(cmd)
	cmd = '{0}/bin/python setup.py develop'.format(venv)
	snakes.util.run_cmd(cmd)

if __name__ == '__main__':
	main()
