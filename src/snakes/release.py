#!/usr/bin/env python

import argparse
import ConfigParser
import os
from os.path import abspath, exists, expanduser, join
import shutil
import subprocess
import sys

import boto
import boto.s3.key
import git
import requests

venv = os.environ.get('VIRTUALENV_HOME', abspath('vendor/python'))
cache = os.environ.get('VENV_CACHE_HOME', abspath('vendor/cache'))
home = os.environ.get("SNAKEGIT_HOME", expanduser('~/.snakegit'))
bucket_name = os.environ.get('GEARBOX_BUCKET', 's3_ops')

def _python_bin():
    '''Return path to virtualenv python'''
    if not exists(venv):
        msg = "Missing virtualenv: have you run 'build'? (looked in: {0})"
        raise RuntimeError(msg.format(venv))
    return abspath("{0}/bin/python".format(venv))

def upload():
    if exists(abspath('./setup.py')) \
            and not exists(abspath('./_gb')):
        upload_pypi()
    if exists(abspath('./_gb')):
        upload_gearbox_app()

def upload_pypi():
    repo = git.Repo(home)
    reader = repo.config_reader()
    uid = reader.get('pypi', 'user')
    key = reader.get('pypi', 'key')
    filename_cmd = "ls -rt dist/|tail -1"
    upload_file = subprocess.check_output(filename_cmd, shell=True).strip()
    with open(abspath(join('dist',upload_file)), 'r') as f:
        r = requests.post("https://repo.n-s.us/upload", auth=(uid, key),
                          files={'upload_file': (upload_file, f) },
                          verify=False)
        if r.status_code == 201:
            print "Uploaded successfully"
        else:
            print "Error uploading package"

def upload_gearbox_app():
    parser = ConfigParser.RawConfigParser()
    parser.read(abspath('snake.cfg'))
    name = parser.get('release', 'name')
    version = parser.get('release', 'version')
    s3_conn = boto.connect_s3()
    bucket = s3_conn.get_bucket(bucket_name)
    key = boto.s3.key.Key(bucket)
    key.key = '{0}/{1}.tar.gz'.format(name, version)
    key.set_contents_from_filename('gearbox_dist/{0}.tar.gz'.format(version))
    print "Uploaded gearbox update"

def python_sdist():
    print "Building python source distribution"
    cmd = [_python_bin(), "setup.py", "sdist"]
    subprocess.call(cmd)

def gearbox_dist():
    print "Build gearbox distribution"
    cmd = [_python_bin(), "setup.py", "install"]
    subprocess.call(cmd)
    cmd = ["{0}/bin/virtualenv".format(home),
            "--relocatable",
            venv]
    subprocess.call(cmd)
    if exists('./gearbox'):
        shutil.rmtree('./gearbox')
    os.mkdir('./gearbox')
    cmd = ["rsync",
        "-arv",
        "{0}/".format(venv),
        "gearbox/"]
    subprocess.call(cmd)
    cmd = ["rsync",
        "-arv",
        "_gb/gbtemplate/",
        "gearbox/gbtemplate/"]
    subprocess.call(cmd)
    cwd = os.getcwd()
    if not exists('./gearbox_dist'):
        os.mkdir('./gearbox_dist')
    parser = ConfigParser.RawConfigParser()
    parser.read(abspath('./snake.cfg'))
    os.chdir('gearbox')
    version = parser.get('release', 'version')
    cmd = ["tar",
            "-czvf",
            "../gearbox_dist/{0}.tar.gz".format(version),
            "."]
    subprocess.call(cmd)
    os.chdir(cwd)

def create():
    if exists(abspath('./setup.py')) \
            and not exists(abspath('./_gb')):
        python_sdist()
    if exists(abspath('./_gb')):
        gearbox_dist()


def main():
    """docstring for main"""
    if len(sys.argv) == 1:
        print "either specify create or upload"
        sys.exit(1)
    if sys.argv[1] == 'create':
        create()
    elif sys.argv[1] == 'upload':
        upload()
    else:
        print "Unknown release task"
        sys.exit(1)


if __name__ == '__main__':
    main()
