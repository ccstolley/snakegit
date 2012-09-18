#!/usr/bin/env python

import argparse
import os
import os.path
import shutil
import subprocess
import git
import sys

home = os.environ.get('SNAKEGIT_HOME', os.path.expanduser('~/.snakegit'))
venv = os.path.abspath(os.environ.get('VIRTUALENV_HOME', 'vendor/python'))
cache = os.path.abspath(os.environ.get('VENV_CACHE_HOME', 'vendor/cache'))

def sync():
    shutil.rmtree(cache)
    os.makedirs(cache)
    repo = git.Repo(home)
    reader = repo.config_reader()
    if not reader.has_section('pypi'):
        print "Pypi is not set up yet."
        sys.exit(1)
    uid = reader.get('pypi', 'user')
    password = reader.get('pypi', 'key')
    cmd = "pip install --no-install -d vendor/cache/ --no-deps -i https://{0}:{1}@repo.n-s.us/simple -r requirements.txt".format(uid, password)
    subprocess.call(cmd, shell=True)
    if os.path.exists(os.path.abspath('./test-requirements')):
        cmd = "yes w | pip install --no-install -d vendor/cache/ --no-deps -r test-requirements.txt"
        subprocess.call(cmd, shell=True)


def main():
    """docstring for main"""
    if len(sys.argv) == 1:
        sync()
    parser = argparse.ArgumentParser()

if __name__ == '__main__':
    main()
