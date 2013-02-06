#!/usr/bin/env python

import argparse
import os
from os.path import abspath, exists, expanduser, join
import re
import subprocess
import sys

import git


REQ_PATTERN = re.compile(r"(?P<name>.+)(?P<operator>[><=~+]=)(?P<version>.*)")


def requirements(filename):
    "Generator for iterating the contents of a requirements file"
    with open(filename, "r") as fp:
        _requirements(fp.read())


def _requirements(requirements_string):
    for package in requirements_string.strip().split("\n"):
        yield REQ_PATTERN.match(package).groupdict()


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

    def pip_fetch(self, name, version, operator):
        print "Install: %s ver. %s" % (name, version)

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
            "".join([name, operator, version])
            ]
        p2 = subprocess.Popen(cmd)
        p2.communicate()

    def cached_package_file(self, name, version, operator):
        ''' Operator isn't currently used '''

        for pattern in ("%s-%s.tar.gz", "%s-%s.tgz", "%s-%s.zip"):
            package_file = join(self.cache, pattern % (name, version))
            if exists(package_file):
                return package_file
        return None

    def sync(self):
        if not exists(self.cache):
            os.makedirs(self.cache)

        for requirement in requirements("requirements.txt"):
            if self.cached_package_file(**requirements) is None:
                self.pip_fetch(**requirements)

        if exists(abspath('./test-requirements')):
            with open("test-requirements.txt", "r") as fp:
                for package in fp:
                    name, version = package.split("==")
                    self.pip_fetch(name, version, "==")


def main():
    """docstring for main"""
    if len(sys.argv) == 1:
        DependenciesTarget().sync()
    argparse.ArgumentParser()


if __name__ == '__main__':
    main()
