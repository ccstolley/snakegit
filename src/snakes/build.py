#!/usr/bin/env python

import subprocess
import os
import os.path
import sys

def main():
    """docstring for main"""
    if 'VIRTUALENV_HOME' in os.environ:
        venv = os.environ['VIRTUALENV_HOME']
    else:
        venv = 'vendor/python'
    if 'VENV_CACHE_HOME' in os.environ:
        cache = os.environ['VENV_CACHE_HOME']
    else:
        cache = os.path.abspath('vendor/cache')
    home = os.environ.get("SNAKEGIT_HOME", os.path.expanduser('~/.snakegit'))
    if not os.path.exists(os.path.join(venv, 'bin', 'python')):
        cmd = [
                os.path.join(home, 'bin', 'virtualenv'),
                '--distribute',
                venv
                ]
        subprocess.call(cmd)
    cmd = [
            '{0}/bin/pip'.format(venv),
            'install',
            '--find-links=file://{0}'.format(cache),
            '--no-index',
            '--index-url=file:///dev/null',
            '--no-deps',
            '-r',
            'requirements.txt'
            ]
    subprocess.call(cmd)

if __name__ == '__main__':
    main()
