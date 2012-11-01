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
import tarfile


SPLIT_REQS = re.compile("==|>=|>|<=|<")
OPERATORS  = ["==", ">=", "<=", ">", "<"]


def get_requirements(dep):
    """
    _get_requirements_

    Look in vendor/cache to find a dependency requirement
    and read the tarfile looking for a requirements file

    """
    tarfile_name = "{0}".format(dep.dependency)
    tarfile_str = "{0}-{1}".format(tarfile_name,dep.version)
    tarfile_path = "{0}.tar.gz".format(tarfile_str)

    req_file = "{0}/requirements.txt".format(tarfile_str)
    tarfile_path = os.path.join("vendor", "cache", tarfile_path)

    if os.path.exists(tarfile_path):
        tf = tarfile.open(tarfile_path)
        if req_file not in tf.getnames():
            print "no requirements.txt in", dep.dependency
            return []
        reqs = tf.extractfile(req_file)
        content = reqs.read()
        return parse_requirements(content, dep.dependency)
    else:
        msg = "Cant find tarfile for {0} {1} ".format(dep.dependency, dep.version)
        msg +=  "expected to find: {0}".format(tarfile_path)
        print msg
        return []


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
    my_reqs = read_requirements_file()

    req_table = {}
    for req in my_reqs:
        req_table.setdefault(req.dependency, [req] )
    update_table = {}
    update_table.update(req_table)

    for dep, dep_instance in req_table.iteritems():
        for dep_req in get_requirements(dep_instance[0]):
            req_name = dep_req.dependency
            if req_name not in update_table:
                update_table[req_name] = [ dep_req ]
            if dep_req not in update_table[req_name]:
                update_table[req_name].append(dep_req)
    return update_table


def check():
    """
    _check_

    requirement version conflict check.
    Parses

    """
    req_table = build_req_table()
    exit_code = 0
    for key, versions in req_table.iteritems():
        msg = "dependency on {0} versions {1}".format(key, " ".join([ x.version for x in versions ]))
        print msg
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
