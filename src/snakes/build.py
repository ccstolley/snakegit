#!/usr/bin/env python

import argparse
import os
import os.path
import sys

import git
import sh

from pkg_resources import Requirement, WorkingSet

EMPTY_DEFAULT = {'args': []}


def version_in_working_set(requirement, working_set):
    installed = working_set.by_key.get(requirement.key)
    return installed is not None and installed in requirement


def find_required(venv, file_):
    pkgdir = os.path.join(os.path.abspath(venv), "lib/python2.7/site-packages")
    working_set = WorkingSet([pkgdir])
    #We need a version of nose & pylint, preferably our version, but if someone
    # insists on adding it to requirements.txt, we should accomodate them.
    nose_fulfilled = False
    pylint_fulfilled = False
    with open(file_, 'r') as fp:
        required = [Requirement.parse(req) for req in fp \
                    if not req.startswith("#")]
        requested = []
        for requirement in required:
            if requirement.project_name == 'nose':
                nose_fulfilled = True
            if requirement.project_name == 'pylint':
                pylint_fulfilled = True
            if not version_in_working_set(requirement, working_set):
                requested.append(requirement)

    if not nose_fulfilled:
        requirement = Requirement.parse('nose==1.2.1')
        if not version_in_working_set(requirement, working_set):
            requested.append(requirement)
    if not pylint_fulfilled:
        requirement = Requirement.parse('pylint==0.26.0')
        if not version_in_working_set(requirement, working_set):
            requested.append(requirement)
    return requested


def install_required(venv, cache, index, requirements):
    pip = sh.Command("{0}/bin/pip".format(venv))
    print "Installing: %s" % unicode(requirements)
    cache = "file://{0}".format(cache)
    for line in pip.install(*requirements, find_links=cache, index_url=index,
                            build="build", download_cache=cache,
                            exists_action="i", _iter=True, upgrade=True):
        sys.stdout.write(line)


def main():
    """docstring for main"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--site-packages',
                        action='store_const',
                        const={
                            'args': ['--system-site-packages']
                        },
                        default=EMPTY_DEFAULT,
                        help='Include Site packages in the venv.')
    args = parser.parse_args()
    venv_args = args.site_packages['args']
    venv_args.append('--distribute')
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
        for line in virtualenv(venv, venv_args, prompt="({0})".format(os.getcwd().split('/')[-1]),
                _iter=True):
            sys.stdout.write(line)

    repo = git.Repo(home)
    reader = repo.config_reader()
    if not reader.has_section('pypi'):
        print "Pypi is not set up yet."
        sys.exit(1)

    need_install = find_required(venv, "requirements.txt")
    if need_install:
        uid = reader.get('pypi', 'user')
        password = reader.get('pypi', 'key')
        index = "https://{0}:{1}@repo.n-s.us/simple".format(uid, password)
        install_required(venv, cache, index, need_install)
    python = sh.Command("{0}/bin/python".format(venv))
    for line in python('setup.py', 'develop'):
        sys.stdout.write(line)

    sh.rm("-rf", "build")

if __name__ == '__main__':
    main()
