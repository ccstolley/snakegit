#!/usr/bin/env python

import os
import os.path
import urllib2
import tempfile
import shutil
import subprocess
import sys


def main():
	"""docstring for main"""
	home = os.environ.get('SNAKEGIT_HOME', os.path.expanduser('~/.snakegit'))
	if not os.path.exists(os.path.join(home, 'bin', 'python')):
		virtualenv_src = urllib2.urlopen('https://raw.github.com/pypa/virtualenv/master/virtualenv.py').read()
		fd, path = tempfile.mkstemp()
		os.write(fd, virtualenv_src)
		os.close(fd)
		if os.path.exists('/tmp/virtualenv.py'):
			os.remove('/tmp/virtualenv.py')

		subprocess.call("python {0} --distribute {1}".format(path, home), shell=True)
		os.remove(path)
	current_dir = os.getcwd()
	os.chdir(home)
	cmd = '{0}/bin/pip install --find-links=file://{1} --no-index --index-url=file:///dev/null --no-deps -r requirements.txt'.format(home, os.path.join(home, 'vendor', 'cache'))
	subprocess.call(cmd, shell=True)
	os.chdir(current_dir)
	try:
		import git
	except ImportError:
		sys.path.append(os.path.join(home, 'lib', 'python2.6', 'site-packages'))
		sys.path.append(os.path.join(home, 'lib', 'python2.7', 'site-packages'))
		import git
	repo = git.Repo(home)
	writer = repo.config_writer(config_level='global')
	writer.set('alias', 'snake', '! {0}/bin/snake'.format(home))
	writer.write()

if __name__ == '__main__':
	main()
