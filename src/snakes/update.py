#!/usr/bin/env python

import os
import os.path

import subprocess

def main():
    """docstring for main"""
    home = os.environ.get('SNAKEGIT_HOME', os.path.expanduser('~/.snakegit'))
    pwd = os.getcwd()
    os.chdir(home)
    subprocess.call('git fetch && git pull')
    cmd = '{0}/bin/pip install --find-links=file://{1} --no-index --index-url=file:///dev/null --no-deps -r requirements.txt'.format(home, os.path.join(home, 'vendor', 'cache'))
    subprocess.call(cmd, shell=True)
    subprocess.call('{0}/bin/python setup.py install'.format(home), shell=True)
    subprocess.call("{0}/bin/config".format(home))
    os.chdir(pwd)

if __name__ == '__main__':
    main()
