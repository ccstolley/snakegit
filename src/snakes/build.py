#!/usr/bin/env python

import snakes.util
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
		cache = 'vendor/cache'
	home = os.environ.get("SNAKEGIT_HOME", os.path.expanduser('~/.snakegit'))
	if not os.path.exists(os.path.join(venv, 'bin', 'python')):
		snakes.util.runcmd('{0} --distribute {1}'.format(os.path.join(home, 'bin', 'virtualenv'), venv))
	cmd = '{0}/bin/pip install --find-links=file://{1} --no-index --index-url=file:///dev/null --no-deps -r requirements.txt'.format(venv, cache)
	snakes.util.run_cmd(cmd)
	cmd = '{0}/bin/python setup.py develop'.format(venv)
	snakes.util.run_cmd(cmd)

if __name__ == '__main__':
	main()
