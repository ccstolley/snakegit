#!/usr/bin/env python

import argparse
import os
import os.path
import shutil
import subprocess
import re
import sys
import urlparse

import git
import yolk.pypi

home = os.environ.get('SNAKEGIT_HOME', os.path.expanduser('~/.snakegit'))
venv = os.path.abspath(os.environ.get('VIRTUALENV_HOME', 'vendor/python'))
cache = os.path.abspath(os.environ.get('VENV_CACHE_HOME', 'vendor/cache'))

cheese_shop = yolk.pypi.CheeseShop()

def sync():
    if not os.path.exists(cache):
        os.makedirs(cache)
    repo = git.Repo(home)
    reader = repo.config_reader()
    if not reader.has_section('pypi'):
        print "Pypi is not set up yet."
        sys.exit(1)
    uid = reader.get('pypi', 'user')
    password = reader.get('pypi', 'key')

    os.path.exists(os.path.join('vendor','cache', urlparse.urlparse(dl).path.split('/')[-1]))
    cmd = [
            "pip",
            'install',
            '--no-install',
            '-d',
            'vendor/cache/',
            '--no-deps',
            '--use-mirrors',
            '--extra-index-url https://{0}:{1}@repo.n-s.us/simple'.format(uid,password),
            '-r',
            'requirements.txt'
            ]
    subprocess.call(cmd)
    if os.path.exists(os.path.abspath('./test-requirements')):
        cmd = [
                'pip',
                'install',
                '--no-install',
                '-d',
                'vendor/cache/',
                '--no-deps',
                '-r',
                'test-requirements.txt'
                ]
        subprocess.call(cmd)


def main():
    """docstring for main"""
    if len(sys.argv) == 1:
        sync()
    parser = argparse.ArgumentParser()

if __name__ == '__main__':
    main()
