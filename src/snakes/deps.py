#!/usr/bin/env python

import argparse
import os
import os.path
import shutil
import subprocess
import sys

if 'VIRTUALENV_HOME' in os.environ:
    venv = os.environ['VIRTUALENV_HOME']
else:
    venv = 'vendor/python'
if 'VENV_CACHE_HOME' in os.environ:
    cache = os.environ['VENV_CACHE_HOME']
else:
    cache = os.path.abspath('vendor/cache')

def sync():
    shutil.rmtree(cache)
    os.makedirs(cache)
    cmd = "pip install --no-install -d vendor/cache/ --no-deps -r requirements.txt"
    subprocess.call(cmd, shell=True)
    if os.path.exists(os.path.abspath('./test-requirements')):
        cmd = "yes w | pip install --no-install -d vendor/cache/ --no-deps -r test-requirements.txt"
        subprocess.call(cmd, shell=True)


def main():
    """docstring for main"""
    if len(sys.argv) == 1:
        sync()
    parser = argparse.ArgumentParser()

if __name__ == '__main__':
    main()
