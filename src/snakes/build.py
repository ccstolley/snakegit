#!/usr/bin/env python

import os
import os.path
import sys

import git
import sh

def main():
    """docstring for main"""
    home = os.environ.get("SNAKEGIT_HOME", os.path.expanduser('~/.snakegit'))
    virtualenv = sh.Command("{0}/bin/virtualenv".format(home))
    if 'VIRTUALENV_HOME' in os.environ:
        venv = os.environ['VIRTUALENV_HOME']
    else:
        venv = 'vendor/python'
    if 'VENV_CACHE_HOME' in os.environ:
        cache = os.environ['VENV_CACHE_HOME']
    else:
        cache = os.path.abspath('vendor/cache')
    if not os.path.exists(os.path.join(venv, 'bin', 'python')):
        for line in virtualenv(venv, '--distribute', prompt="({0})".format(os.getcwd().split('/')[-1]),
                _iter=True):
            sys.stdout.write(line)
            
    repo = git.Repo(home)
    reader = repo.config_reader()
    if not reader.has_section('pypi'):
        print "Pypi is not set up yet."
        sys.exit(1)
    uid = reader.get('pypi', 'user')
    password = reader.get('pypi', 'key')

    pip = sh.Command("{0}/bin/pip".format(venv))
    with open('requirements.txt', 'r') as handle:
        for req in handle.readlines():
            if not req.startswith("#"):
                for line in pip.install(req, find_links="file://{0}".format(cache),
                        index_url="https://{0}:{1}@repo.n-s.us/simple".format(uid, password), 
                        build="build", download_cache=cache, exists_action="i",
                        _iter=True):
                    sys.stdout.write(line)
    sh.rm("-rf", "build")

if __name__ == '__main__':
    main()
