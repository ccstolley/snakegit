#!/usr/bin/env python

import argparse
import os
import os.path
import subprocess
import sys

import snakes.util


def unit(args):
    venv = os.environ.get('VIRTUALENV_HOME', 'vendor/python')
    cache = os.environ.get('VENV_CACHE_HOME', 'vendor/cache')
    home = os.environ.get('SNAKEGIT_HOME', os.path.expanduser('~/.snakegit'))
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--xunit',
          action='store_const',
          const='--with-xunit --xunit-file={0}/nosetests.xml',
          default='',
          help="Generate XUnit formatted report")
    parser.add_argument("-c", '--coverage',
          action='store_const',
          const='--with-coverage --cover-xml --cover-xml-file={0}/coverage.xml',
          default='',
          help="Generate a test coverage report")
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

    if os.path.exists(os.path.join(os.getcwd(), 'test-requirements.txt')):
        cmd = ['{0}/bin/pip'.format(home),
               'install',
               '--find-links=file://{0}'.format(cache),
               '--no-index',
               '--index-url=file:///dev/null',
               '--no-deps',
               '-r',
               'test-requirements.txt']
        subprocess.call(cmd)
    if args.package is not None and args.package != '':
        args.package = '--cover-package={0}'.format(args.package)

    if not os.path.exists(args.output):
        os.makedirs(args.output)
    python_path = 'test_configs:src:.:{0}/lib/python2.6/site-packages:{0}/lib/python2.7/site-packages'.format(venv)
    cmd = "{0}/bin/nosetests {1} {2} {3} {4}".format(
          home,
          args.xunit.format(args.output),
          args.coverage.format(args.output),
          args.package,
          args.directory)
    return subprocess.call(cmd.split(), env={"PYTHONPATH": python_path})


def functional():
    if os.path.exists('tests/functional'):
        for dirname, dirnames, filenames in os.walk('tests/functional'):
            for filename in filenames:
                snakes.util.run_cmd(os.path.join(dirname, filename))


def main():
    """docstring for main"""
    return unit(sys.argv[1:])

if __name__ == '__main__':
    sys.exit(main())
