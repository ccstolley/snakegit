#!/usr/bin/env python

import argparse
import ConfigParser
import git
import os
import sh
import sys


def bump_req(requirement, repo_name, package_path):
    print 'Upgrading {0} to its latest version'.format(requirement)
    sh.git.checkout('develop')
    version = _get_version_from_git(repo_name, package_path)
    # TODO(jdrake): when our pypi SSL cert is updated, switch version function
    # version = _get_version_from_pypi(requirement)
    _set_requirement_version(requirement, version)
    _push_change(requirement)
    print '{0} upgraded to version {1}'.format(requirement, version)


def _get_version_from_git(repo_name, package_path):
    '''Clone git repo and extract version string from a package's snake.cfg'''
    repo_url = 'git@github.com:NarrativeScience/{0}.git'.format(repo_name)
    repo_tmp = os.path.join('/tmp', repo_name)
    sh.rm('-rf', repo_tmp)
    sh.git.clone(repo_url, repo_tmp, depth=1)
    config_file = os.path.join(repo_tmp, package_path, 'snake.cfg')
    version = _parse_version_from_cfg(config_file)
    return version


def _parse_version_from_cfg(*args):
    return _parse_cfg('version', *args)


def _parse_name_from_cfg(*args):
    return _parse_cfg('name', *args)


def _parse_cfg(key, config_file):
    config = ConfigParser.RawConfigParser()
    config.read(config_file)
    value = config.get('release', key)
    return value


# def _get_version_from_pypi(requirement):
#     pypi_index = _get_pypi_index()
#     sh.pip.list(index_url=pypi_index, outdated=True)
#     return 'love'


# def _get_pypi_index():
#     '''Build URL for NS pypi with basic auth'''
#     home = os.environ.get('SNAKEGIT_HOME', os.path.expanduser('~/.snakegit'))
#     repo = git.Repo(home)
#     reader = repo.config_reader()
#     if not reader.has_section('pypi'):
#         print 'Pypi is not set up yet.'
#         sys.exit(1)
#     uid = reader.get('pypi', 'user')
#     password = reader.get('pypi', 'key')
#     index = "https://{0}:{1}@repo.n-s.us/simple".format(uid, password)
#     return index


def _set_requirement_version(requirement, version):
    '''Set the version string for a given requirement'''
    req_file = './requirements.txt'
    with open(req_file) as f:
        new_lines = []
        for line in f.readlines():
            if line.strip().split('==')[0] == requirement:
                new_line = '{0}=={1}'.format(requirement, version)
            else:
                new_line = line.strip()
            new_lines.append(new_line)
    with open(req_file, 'w') as f:
        f.write('\n'.join(new_lines))


def _push_change(requirement):
    sh.git.add('-A')
    name = _parse_name_from_cfg('./snake.cfg')
    message = 'AUTOBUILD bumped {0} {1} requirement'.format(name, requirement)
    sh.git.commit(message=message)
    sh.git.push()


def main():
    parser = argparse.ArgumentParser(description='Bumps REQUIREMENT in requirements.txt to its latest released version')
    parser.add_argument('requirement', help='name of package requirement')
    parser.add_argument('-r', '--repo-name', help='repository name for requirement', required=True)
    parser.add_argument('-p', '--package-path', help='path to package from repo root', default='.')
    args = parser.parse_args()
    bump_req(args.requirement, args.repo_name, args.package_path)


if __name__ == '__main__':
    sys.exit(main())
