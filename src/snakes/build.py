#!/usr/bin/env python

import subprocess
import os
import os.path

def main():
	"""docstring for main"""
	if 'VIRTUALENV_HOME' in os.environ:
		venv = os.environ['VIRTUALENV_HOME']
	else:
		venv = 'vendor/python'
	if 'VENV_CACHE_HOME' in os.environ:
		cache = os.environ['VENV_CACHE_HOME']
	else:
		cache = os.path.abspath('vendor/cache')
	home = os.environ.get("SNAKEGIT_HOME", os.path.expanduser('~/.snakegit'))
	if not os.path.exists(os.path.join(venv, 'bin', 'python')):
		cmd = '{0} --distribute {1}'.format(os.path.join(home, 'bin', 'virtualenv'), venv)
		subprocess.call(cmd, shell=True)
	cmd = '{0}/bin/pip install --find-links=file://{1} --no-index --index-url=file:///dev/null --no-deps -r requirements.txt'.format(venv, cache)
	subprocess.call(cmd, shell=True)
	cmd = '{0}/bin/python setup.py develop'.format(venv)
	subprocess.call(cmd, shell=True)

if __name__ == '__main__':
	main()
