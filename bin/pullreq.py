#!/usr/bin/env python 
"""Create a pull request by pushing the current branch."""


import argparse
import json
import subprocess
import sys
import urllib2


BASE_URL = 'https://api.github.com'
ORIGIN_LINE_START = 'Push  URL:'
ORGANIZATION = 'NarrativeScience'


def get_token():
    """Retrieve the oauth token."""
    token, _ = subprocess.Popen(
            "git config --get github.token",
            shell=True,
            stdout=subprocess.PIPE).communicate()
    return token.strip()


def get_branch():
    """Get the current local branch."""
    branch_name, _ = subprocess.Popen(
            "git symbolic-ref HEAD 2>/dev/null",
            shell=True,
            stdout=subprocess.PIPE).communicate()
    if branch_name:
        return branch_name.strip().replace("refs/heads/", "")
    else:
        return None


def push_branch():
    """Push the given branch."""
    branch = get_branch()
    subprocess.Popen("git push origin %s" % branch, shell=True).wait()


def get_repo_and_user():
    """Call show origin to retrieve the repo and user."""
    origin, _ = subprocess.Popen(
            'git remote show origin',
            shell=True,
            stdout=subprocess.PIPE).communicate()
    for line in origin.split('\n'):
        line = line.strip()
        if line.startswith(ORIGIN_LINE_START):
            origin_line = line[len(ORIGIN_LINE_START):].strip()
            _, user_name_repo = origin_line.split(':')
            user_name, repo = user_name_repo.split('/')
            repo = repo.replace('.git', '')
            return user_name, repo


def create_pull_request(title, body, base, recips):
    """Create the pull request."""
    branch = get_branch
    if branch is None:
        print 'detached head'
        sys.exit(-1)
    else:
        user, repo = get_repo_and_user()
        body = body + '\n' + ' '.join('@' + recip for recip in recips)
        head = get_branch()
        args = {'title': title,
                'body': body,
                'head': head,
                'base': base}
        url = BASE_URL + '/repos/%s/%s/pulls' % (user, repo)
        try:
            response = make_github_request(url=url, data=json.dumps(args))
            return response.read()
        except urllib2.HTTPError as response:
            print response.read()
            sys.exit(-1)


def make_github_request(*args, **kwargs):
    """Send an authorization token in a github api request."""
    token = get_token()
    kwargs.setdefault('headers', {}).update(
            {'Authorization': 'token %s' % token})
    req = urllib2.Request(*args, **kwargs)
    return urllib2.urlopen(req)


def get_args(organization, members):
    """Parse cmdline args."""
    parser = argparse.ArgumentParser(description='Make a pull request.')
    parser.add_argument(
            '--title',
            dest='title',
            required=True,
            help='pull request title')
    parser.add_argument(
            '--body',
            dest='body',
            required=True,
            help='pull request description')
    parser.add_argument(
            '--base',
            dest='base',
            default='master',
            required=False,
            help='branch to create the pull request against')
    parser.add_argument(
            '--no-push',
            dest='push',
            default=True,
            action='store_false',
            required=False,
            help='do not perform a push before creating the pull request')

    class ListMembers(argparse.Action):
        """List members of the organization and exit"""
        def __call__(*args, **kwargs):
            """List members of the organization and exit"""
            print '\n'.join(members)
            sys.exit(0)

    parser.add_argument(
            '--list-members',
            dest='get_members',
            default=False,
            nargs=0,
            required=False,
            action=ListMembers,
            help=('list members of the organization %s and exit' %
                organization))

    members_dict = {member: None for member in members}
    def parse_recips(arg):
        """Parse the list of recipients."""
        recips = arg.split(',')
        clean_recips = []
        for recip in recips:
            recip = recip.strip()
            if recip not in members_dict:
                raise argparse.ArgumentTypeError(
                        '%s is not a member of %s' % (recip, organization))
            clean_recips.append(recip)
        return clean_recips

    parser.add_argument(
            '--to',
            dest='recips',
            type=parse_recips,
            required=True,
            help='comma-seperated list of pull request recipients')

    return parser.parse_args()


def get_members(org):
    """Return the list of member in organization @org."""
    url = BASE_URL + '/orgs/%s/members' % org
    response = make_github_request(url)
    members = json.loads(response.read())
    return [member['login'] for member in members]


def main():
    """Parse the args and create a pull request."""
    members = get_members(ORGANIZATION)
    args = get_args(ORGANIZATION, members)
    if args.push:
        push_branch()
    create_pull_request(args.title, args.body, args.base, args.recips)

if __name__ == '__main__':
    main()
