#!/usr/bin/env python
"""
_requirements_

Command handler for requirements related commands.
Developer would use this to first validate their requirements, then
look for conflicts in dependent packages, and then after resolving
any conflicts, update the requirements.txt in this package to keep
all dependencies in sync

Implements:

- validate - scan the requirements.txt in this package for problems
- conflicts - check for conflicts in requirements of dependent packages
- update - if no conflicts, update the requirements.txt in this package
  to include all the same requirements of the dependent packages

"""
import os
import re
import sys
import json
import base64
import subprocess
import requests


SPLIT_REQS = re.compile("==|>=|>|<=|<")
OPERATORS  = ["==", ">=", "<=", ">", "<"]


def get_token():
    """Retrieve the oauth token."""
    token, _ = subprocess.Popen(
            "git config --get github.token",
            shell=True,
            stdout=subprocess.PIPE).communicate()
    return token.strip()


def list_ns_repos(token):
    """
    _list_ns_repos_

    Get a list of NS Repo names from the github API
    """
    url = "https://api.github.com/orgs/NarrativeScience/repos"
    headers = {"Authorization": "token {0}".format(token)}
    resp = requests.get(url, headers = headers)
    data = json.loads(resp.text)
    repos = [ d['name'] for d in data if d['private'] ]
    return repos


def get_requirements(repo, token):
    """
    _get_requirements_

    Grab the requirements.txt file for the repo provided

    """
    req_url = "https://api.github.com/repos/NarrativeScience/"
    req_url += repo
    req_url += "/contents/requirements.txt"
    resp = requests.get(req_url, headers = {
        "Authorization" : "token {0}".format(token)
        })
    data = json.loads(resp.text)
    reqs_text = base64.decodestring(data['content'])
    return parse_requirements(reqs_text, repo)


class VersionReq(object):
    """
    container object for a version dependency.
    """
    def __init__(self):
        super(VersionReq, self).__init__()
        self.package = None
        self.operator = None
        self.version = None
        self.dependency = None

    def __eq__(self, lhs):
        """equality based on version"""
        return self.version == lhs.version


def parse_requirements(req_str, pkg = None):
    """
    _parse_requirements_

    convert requirements string into a list of
    VersionReq objects
    """
    result = []
    for line in req_str.split("\n"):
        if line.strip() == '': continue
        if line.strip().startswith("#"): continue
        elems = SPLIT_REQS.split(line)
        if len(elems) == 1:
            elems = [elems[0], None]
        op_token = None
        for oper in OPERATORS:
            if oper in line:
                op_token = oper
                break
        req = VersionReq()
        req.dependency = elems[0]
        req.version = elems[1]
        req.operator = op_token
        req.package = pkg
        result.append(req)
    return result


def read_requirements_file():
    """
    _read_requirements_file_

    Load in the requirements file in this package,
    assumed to be at pwd/requirements.txt

    """
    reqs_file = os.path.join(os.getcwd(), "requirements.txt")
    with open(reqs_file, 'r') as handle:
        content = handle.read()
    return parse_requirements(content)


def update():
    """
    _update_

    """
    outcome = check()
    if outcome:
        msg = "Conflicts found in requirements.\n"
        msg += "Please fix them before running update\n"
        print msg
        return 1
    msg = "No conflicts found, updating requirements.txt...\n"
    content = ""
    reqs = build_req_table()
    for req, reqd in reqs.iteritems():
        version = reqd[0].version
        if version != None:
            line = "{0}=={1}\n".format(req, version)
        else:
            line = "{0}\n".format(req)
        content += line
        msg += line

    print msg
    with open("requirements.txt", 'w') as handle:
        handle.write(content)
    return 0


def validate():
    """
    _validate_

    Read requirements.txt for this package and checks for
    all kinds of nasty badness like no specified version

    TODO: check requirements against pip/pypi to make sure they exist

    """
    my_reqs = read_requirements_file()
    exit_code = 0
    for req in my_reqs:
        if req.version == None:
            msg = "Validation Failure: No version required for {0}".format(
                req.dependency)
            exit_code = 1
            print msg
    return exit_code


def build_req_table():
    """
    _build_req_table_

    Parse requirements.txt in this package and search for
    other NS repos that this package depends on.

    This goes one deep, while it could get all recursive,
    that seems like overkill right now...

    Returns

    """
    my_token = get_token()
    our_repos = list_ns_repos(my_token)
    my_reqs = read_requirements_file()
    dependencies = [ x.dependency for x in my_reqs if x.dependency in our_repos]

    req_table = {}
    for req in my_reqs:
        req_table.setdefault(req.dependency, [req] )

    for dep in dependencies:
        for dep_req in get_requirements(dep, my_token):
            req_name = dep_req.dependency
            if req_name not in req_table:
                req_table[req_name] = [ dep_req ]
            if dep_req not in req_table[req_name]:
                req_table[req_name].append(dep_req)
    return req_table


def check():
    """
    _check_

    requirement version conflict check.
    Parses

    """
    req_table = build_req_table()
    exit_code = 0
    for key, versions in req_table.iteritems():
        if len(versions) > 1:
            msg = "***Version Conflict for {0}***\n".format(key)
            for version in versions:
                if version.package == None:
                    version.package = "this"
                msg += "  {0} package requires version {1}\n".format(
                    version.package, version.version
                    )
            print msg
            exit_code = 1
    return exit_code


def main():
    """main function to dispatch to function based on CL args"""
    if len(sys.argv) == 1:
        print "either specify check or update"
        sys.exit(1)
    if sys.argv[1] == 'update':
        update()
    elif sys.argv[1] == 'conflict':
        sys.exit(check())
    elif sys.argv[1] == 'validate':
        sys.exit(validate())
    else:
        print "Unknown requirements task {0}".format(sys.argv[1])
        sys.exit(1)


if __name__ == '__main__':
    main()
