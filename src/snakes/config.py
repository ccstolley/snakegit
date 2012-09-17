#!/usr/bin/env python

import os
import os.path
import urllib2
import tempfile
import shutil

import snakes.util

import git

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
		snakes.util.run_cmd("python {0} --distribute {1}".format(path, home))
		os.remove(path)
	current_dir = os.getcwd()
	os.chdir(home)
	cmd = '{0}/bin/pip install --find-links=file://{1} --no-index --index-url=file:///dev/null --no-deps -r requirements.txt'.format(home, os.path.join(home, 'vendor', 'cache'))
	snakes.util.run_cmd(cmd)
	os.chdir(current_dir)
	repo = git.Repo(home)
	writer = repo.config_writer(config_level='global')
	writer.set('alias', 'snake', '! {0}/bin/snake'.format(home))
	writer.write()

if __name__ == '__main__':
	main()
