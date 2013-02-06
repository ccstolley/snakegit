#!/usr/bin/env python

import ConfigParser
import glob
import os
import re
from os.path import abspath, exists, expanduser, join
import sh
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
parser = ConfigParser.RawConfigParser()
parser.read(os.path.abspath('snake.cfg'))


def _python_bin():
    '''Return path to virtualenv python'''
    if not exists(venv):
        msg = "Missing virtualenv: have you run 'build'? (looked in: {0})"
        raise RuntimeError(msg.format(venv))
    return abspath("{0}/bin/python".format(venv))


def upload():
    if parser.has_option('release', 'app_and_lib'):
        upload_pypi()
        upload_gearbox_app()
    elif os.path.exists(os.path.abspath('./_gb')):
        upload_gearbox_app()
    elif os.path.exists(os.path.abspath('./setup.py')):
        upload_pypi()
    upload_release_tag()


def upload_pypi():
    repo = git.Repo(home)
    reader = repo.config_reader()
    uid = reader.get('pypi', 'user')
    key = reader.get('pypi', 'key')
    # only grab the tar.gz files since the gearbox create process creates
    # egg files in the dist dirctory. We definitely don't want to upload
    # those. Strip away the 'dist/' part of the path name
    filename_cmd = "ls -rt dist/*.tar.gz | tail -1"
    upload_file = subprocess.check_output(filename_cmd, shell=True).strip()[5:]
    with open(abspath(join('dist', upload_file)), 'r') as f:
        r = requests.post("https://repo.n-s.us/upload", auth=(uid, key),
                          files={'upload_file': (upload_file, f)},
                          verify=False)
        if r.status_code == 201:
            print "Uploaded successfully"
        else:
            print "Error uploading package"
            print r.status_code
            print r.text
            sys.exit(1)


def upload_gearbox_app():
    name = parser.get('release', 'name')
    version = parser.get('release', 'version')
    s3_conn = boto.connect_s3()
    bucket = s3_conn.get_bucket(bucket_name)
    key = boto.s3.key.Key(bucket)
    key.key = '{0}/{1}.tar.gz'.format(name, version)
    key.set_contents_from_filename('gearbox_dist/{0}.tar.gz'.format(version))
    print "Uploaded gearbox update"


def upload_release_tag():
    version = parser.get('release', 'version')
    sh.git('tag', version)
    sh.git('push', 'origin', version)


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

    if parser.has_option('release', 'flask_blueprint_root'):
        for dir_name in ["static", "templates"]:
            pattern = re.compile("src\/(.*)\/{0}".format(dir_name))
            for path in glob.glob("src/*/{0}".format(dir_name)):
                subdir = pattern.match(path).groups()[0]
                trail = "{0}/{1}/".format(subdir, dir_name)
                if not os.path.exists("gearbox/{0}".format(subdir)):
                    os.mkdir("gearbox/{0}".format(subdir))
                command = ['rsync', '-arv', "src/{0}".format(trail),
                        "gearbox/{0}".format(trail)]
                subprocess.call(command)

    if not exists('./gearbox_dist'):
        os.mkdir('./gearbox_dist')
    os.chdir('gearbox')
    version = parser.get('release', 'version')
    cmd = ["tar",
            "-czvf",
            "../gearbox_dist/{0}.tar.gz".format(version),
            "."]
    subprocess.call(cmd)
    os.chdir(cwd)


def create():
    if parser.has_option('release', 'app_and_lib'):
        python_sdist()
        gearbox_dist()
    elif exists(os.path.abspath('./setup.py')) \
            and not os.path.exists(os.path.abspath('./_gb')):
        python_sdist()
    elif exists(os.path.abspath('./_gb')):
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
