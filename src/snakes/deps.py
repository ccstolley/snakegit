#!/usr/bin/env python

import argparse
import os
from os.path import abspath, exists, expanduser
import subprocess
import sys

import git


class DependenciesTarget(object):

    home = os.environ.get('SNAKEGIT_HOME', expanduser('~/.snakegit'))
    venv = abspath(os.environ.get('VIRTUALENV_HOME', 'vendor/python'))
    cache = abspath(os.environ.get('VENV_CACHE_HOME', 'vendor/cache'))

    def __init__(self):
        repo = git.Repo(self.home)
        reader = repo.config_reader()
        if not reader.has_section('pypi'):
            print "Pypi is not set up yet."
            sys.exit(1)
        self.uid = reader.get('pypi', 'user')
        self.password = reader.get('pypi', 'key')

    def pip_fetch(self, fname):
        cmd = [
            "pip",
            'install',
            '--no-install',
            '-d',
            'vendor/cache/',
            '--use-mirrors',
            "-i",
            "https://{0}:{1}@repo.n-s.us/simple/".format(self.uid,
                                                         self.password),
            "-r %s" % fname
            ]
        p2 = subprocess.Popen(cmd)
        p2.communicate()

    def sync(self):
        if not exists(self.cache):
            os.makedirs(self.cache)

        self.pip_fetch("requirements.txt")
        if exists(abspath('./test-requirements')):
            self.pip_fetch("test-requirements.txt")


def main():
    """docstring for main"""
    if len(sys.argv) == 1:
        DependenciesTarget().sync()
    argparse.ArgumentParser()


if __name__ == '__main__':
    main()
