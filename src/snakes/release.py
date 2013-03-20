import ConfigParser
import glob
import fnmatch
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


def _set_dunder_version(version):
    for root, dirnames, filenames in os.walk('src'):
        for filename in fnmatch.filter(filenames, '__init__.py'):
            with open(os.path.join(root, filename)) as handle:
                new_content = []
                updated = False
                for line in handle.readlines():
                    to_add = line.strip()
                    if '__version__' in line:
                        updated = True
                        to_add = re.sub(r"__version__\s=\s'.*'",
                            "__version__ = '{0}'".format(version),
                            line.strip())
                    new_content.append(to_add)
                if not updated:
                    new_content.append("__version__ = '{0}'".format(version))
            with open(os.path.join(root, filename), 'w') as handle:
                handle.write("\n".join(new_content))
            print os.path.join(root, filename)
            return os.path.join(root, filename)


def _python_bin():
    '''Return path to virtualenv python'''
    if not exists(venv):
        msg = "Missing virtualenv: have you run 'build'? (looked in: {0})"
        raise RuntimeError(msg.format(venv))
    return abspath("{0}/bin/python".format(venv))


def upload(upload_release_file):
    upload_release_tag()
    if parser.has_option('release', 'app_and_lib'):
        upload_pypi()
        upload_gearbox_app(upload_release_file)
    elif os.path.exists(os.path.abspath('./_gb')):
        upload_gearbox_app(upload_release_file)
    elif os.path.exists(os.path.abspath('./setup.py')):
        upload_pypi()


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


def upload_gearbox_app(upload_release_file):
    name = parser.get('release', 'name')
    version = parser.get('release', 'version')
    s3_conn = boto.connect_s3()
    bucket = s3_conn.get_bucket(bucket_name)
    key = boto.s3.key.Key(bucket)
    key.key = '{0}/{1}.tar.gz'.format(name, version)
    key.set_contents_from_filename('gearbox_dist/{0}.tar.gz'.format(version))
    print "Uploaded gearbox update"
    if upload_release_file:
        key = boto.s3.key.Key(bucket)
        key.key = '{0}/LATEST'.format(name)
        key.set_contents_from_string(version)

def upload_release_tag():
    name = parser.get('release', 'name')
    version = parser.get('release', 'version')
    tag = "%s/%s" % (name, version)
    sh.git('tag', tag)
    sh.git('push', 'origin', tag)


def get_existing_tags():
    """
    Grab all of the tags that exist at the origin.
    """
    collector = []
    for line in sh.git('ls-remote', '--tags'):
        split = line.split('refs/tags/')
        if len(split) >= 1:
            collector.append(split[-1].rstrip())
    return collector
    
def check_release():
    """
    Make sure a release is even possible.
    """
    name = parser.get('release', 'name')
    version = parser.get('release', 'version')
    tag = "%s/%s" % (name, version)
    existing_tags = get_existing_tags()
    if tag in existing_tags:
        msg = "The tag %s already exists. It is not possible"
        msg += " to re-release this version currently. If you "
        msg += "wish to re-release, and you REALLY know what you're doing"
        msg += " then please delete the tag before running again."
        print msg % tag
        sys.exit(1)
    else:
        sys.exit(0)
      
def python_sdist():
    print "Building python source distribution"
    version = parser.get('release', 'version')
    init_path = _set_dunder_version(version)
    print "Bumped and committed dunder version"
    sh.git('add', init_path)
    sh.git.commit(m="'Setting dunder version to {0}'".format(version))
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

    update_release_file = False 
    if len(sys.argv) > 2 and sys.argv[2] == '--update-release-file':
       update_release_file = True; 

    if sys.argv[1] == 'create':
        create()
    elif sys.argv[1] == 'upload':
        upload(update_release_file)
    elif sys.argv[1] == 'check':
        check_release()
    else:
        print "Unknown release task"
        sys.exit(1)


if __name__ == '__main__':
    main()
