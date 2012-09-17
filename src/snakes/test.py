#!/usr/bin/env python

import argparse
import os
import os.path

import snakes.util

def main():
  """docstring for main"""
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

  args = parser.parse_args()

  if os.path.exists(os.path.join(os.getcwd(), 'test-requirements.txt')):
    cmd = '{0}/bin/pip install --find-links=file://{1} --no-index --index-url=file:///dev/null --no-deps -r test-requirements.txt'.format(venv, cache)
    snakes.util.run_cmd(cmd)
  if args.package is not None and args.package != '':
    args.package = '--cover-package={0}'.format(args.package)
  
  if not os.path.exists(args.output):
    os.makedirs(args.output)
  python_path = 'PYTHONPATH=src:.:{0}/lib/python2.6/site-packages:{0}/lib/python2.7/site-packages'.format(venv)
  cmd = "{0} {1}/bin/nosetests {2} {3} {4} {5}".format(
    python_path,
    home,
    args.xunit.format(args.output),
    args.coverage.format(args.output),
    args.package,
    args.directory)
  snakes.util.run_cmd(cmd)
    

if __name__ == '__main__':
  main()
