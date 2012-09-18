#!/usr/bin/env python

import argparse
import os
import os.path
import subprocess
import sys

import git
import requests

venv = os.environ.get('VIRTUALENV_HOME', os.path.abspath('vendor/python'))
cache = os.environ.get('VENV_CACHE_HOME', os.path.abspath('vendor/cache'))
home = os.environ.get("SNAKEGIT_HOME", os.path.expanduser('~/.snakegit'))

def upload():
    parser = argparse.ArgumentParser()
    repo = git.Repo(home)
    reader = repo.config_reader()
    uid = reader.get('pypi', 'user')
    key = reader.get('pypi', 'key')
    upload_file = subprocess.check_output("ls -rt dist/|tail -1", shell=True).strip()
    with open(os.path.abspath(os.path.join('dist',upload_file)), 'r') as f:
        r = requests.post("https://repo.n-s.us/upload", auth=(uid, key), files={'upload_file': f}, verify=False)
    

def main():
    """docstring for main"""
    if len(sys.argv) == 1:
        print "either specify create or upload"
        sys.exit(1)
    if sys.argv[1] == 'create':
        if os.path.exists(os.path.abspath('./setup.py')) \
                and not os.path.exists(os.path.abspath('./_gb')):
            print "Building python source distribution" 
            subprocess.call("{0}/bin/python setup.py sdist".format(venv), shell=True)
    elif sys.argv[1] == 'upload':
        upload()
    else:
        print "Unknown release task"
        sys.exit(1)


if __name__ == '__main__':
    main()
