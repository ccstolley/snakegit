#!/usr/bin/env python

import argparse
import os
import os.path
import subprocess
import sys
import logging

import snakes.util

import sh
logging.basicConfig(level=logging.DEBUG)

def lint(args):

    venv = os.environ.get('VIRTUALENV_HOME', 'vendor/python')
    cache = os.environ.get('VENV_CACHE_HOME', 'vendor/cache/')
    home = os.environ.get('SNAKEGIT_HOME', os.path.expanduser('~/.snakegit'))
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rcfile',
                       help="Location of pylintrc file",
                       default='etc/pylintrc')
    parser.add_argument('-d', '--directory',
                        help='Location of source',
                        default='src')
    parser.add_argument("-f", "--format",
                       help="Pylint format",
                       default="parseable")
    args = parser.parse_args(args)
    pylint_args = [args.directory]
    pylint_kwargs = {'rcfile' : args.rcfile,
                     'output-format' : args.format}
    python_path = [
            '.',
            'src',
            ]
    python_version = ""
    for version in ['2.6', '2.7']:
        candidate_path = '{0}/lib/python{1}/site-packages'.format(venv, version)
        if os.path.exists(candidate_path):
            python_path.append(candidate_path)
            python_version = version
            break
    site_packages = "{0}/lib/python{1}/no-global-site-packages.txt".format(
        venv, python_version)
    prefix_file = "{0}/lib/python{1}/orig-prefix.txt".format(venv,
                                                             python_version)
    if not os.path.exists(site_packages):
        with open(prefix_file) as handle:
            prefix = handle.readline()
            python_path.append("{0}/lib/python{1}/site-packages".format(
                prefix, python_version))
    new_env = os.environ.copy()
    new_env["PYTHONPATH"] = ':'.join(python_path)
    pylint = sh.Command("{0}/bin/pylint".format(home))


    pylint_kwargs['_env'] = new_env
    pylint_kwargs['_err'] = sys.stdout
    try:
        output = pylint(*nose_args, **nose_kwargs)
        return output.exit_code
    except sh.ErrorReturnCode:
        # Don't crash snake when an error is raised.
        return 1




def functional():
    if os.path.exists('tests/functional'):
        for dirname, dirnames, filenames in os.walk('tests/functional'):
            for filename in filenames:
                snakes.util.run_cmd(os.path.join(dirname, filename))


def main():
    """docstring for main"""
    return lint(sys.argv[1:])

if __name__ == '__main__':
    main()
