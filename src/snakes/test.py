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

EMPTY_DEFAULT = {'args': [], 'kwargs': {}}

def unit(args):

    venv = os.environ.get('VIRTUALENV_HOME', 'vendor/python')
    cache = os.environ.get('VENV_CACHE_HOME', 'vendor/cache/')
    home = os.environ.get('SNAKEGIT_HOME', os.path.expanduser('~/.snakegit'))
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--xunit',
            action='store_const',
            const={
                'args': ['--with-xunit',],
                'kwargs': {'xunit-file': "{0}/nosetests.xml", }
                },
            default=EMPTY_DEFAULT,
            help="Generate XUnit formatted report")
    parser.add_argument("-c", '--coverage',
            action='store_const',
            const={
                'args': ['--with-coverage',],
                'kwargs': {}
                },
            default=EMPTY_DEFAULT,
            help="Generate a test coverage report")
    parser.add_argument('-C', '--cover-xml',
            action='store_const',
            const={
                'args': ['--with-coverage', '--cover-xml', ],
                'kwargs': {
                    "cover-xml-file": '{0}/coverage.xml',
                    }
                },
            default=EMPTY_DEFAULT,
            help='Generate a test coverage report as XML')
    parser.add_argument('-p', '--package',
            help="Which package should have coverage measured",
            default='')
    parser.add_argument('-d', '--directory',
            help="Which directory holds the tests",
            default="tests/unit")
    parser.add_argument('-o', '--output',
            help="Which directory should hold the test reports",
            default=os.path.join(os.getcwd(), 'test_reports'))

    args = parser.parse_args(args)

    nose_kwargs = {}
    nose_args = []
    if os.path.exists('test-requirements.txt'):
        pip = sh.Command('{0}/bin/pip'.format(venv))
        _find_links = 'file://{0}'.format(os.path.abspath(cache))
        _test_reqs_file = 'test-requirements.txt'
        print pip.install(find_links=_find_links, r=_test_reqs_file)

    if args.package is not None and args.package != '':
        nose_kwargs['cover-package'] = args.package

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    python_path = [
            '.',
            'test_configs',
            'src',
            ]
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
    nose = sh.Command("{0}/bin/nosetests".format(home))

    for arg in [ args.xunit, args.coverage, args.cover_xml ]:
        nose_args.extend(arg['args'])
        nose_kwargs.update(arg['kwargs'])

    for kwarg in ['xunit-file', 'cover-xml-file']:
        if kwarg in nose_kwargs:
            nose_kwargs[kwarg] = nose_kwargs[kwarg].format(args.output)

    nose_args.append(args.directory)
    nose_kwargs['_env'] = new_env
    nose_kwargs['_err'] = sys.stdout
    try:
        output = nose(*nose_args, **nose_kwargs)
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
    return unit(sys.argv[1:])

if __name__ == '__main__':
    main()
