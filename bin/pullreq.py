#!/usr/bin/env python 
"""Create a pull request by pushing the current branch."""


import argparse
import json
import requests
import subprocess
import sys


BASE_URL = 'https://api.github.com'
ORIGIN_LINE_START = 'Push  URL:'


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
        token = get_token()
        user, repo = get_repo_and_user()
        body = body + '\n' + '\n'.join(recips)
        head = get_branch()
        args = {'title': title,
                'body': body,
                'head': head,
                'base': base}
        headers = {'Authorization': 'token %s' % token}
        url = BASE_URL + '/repos/%s/%s/pulls' % (user, repo)
        response = requests.post(url, data=json.dumps(args), headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print response.text
            sys.exit(-1)


def get_args():
    """Parse cmdline args."""
    parser = argparse.ArgumentParser(description='Make a pull request.')
    parser.add_argument('--title', dest='title', required=True)
    parser.add_argument('--body', dest='body', required=True)
    parser.add_argument(
            '--base', dest='base', default='master', required=False)
    parser.add_argument(
            '--no-push',
            dest='push',
            default=True,
            action='store_false',
            required=False)

    def parse_recips(arg):
        """Parse the list of recipients."""
        recips = arg.split(',')
        clean_recips = []
        for recip in recips:
            recip = recip.strip()
            if not recip.startswith('@'):
                recip = '@' + recip
            clean_recips.append(recip)
        return clean_recips

    parser.add_argument('--to', dest='recips', type=parse_recips, required=True)

    return parser.parse_args()


def main():
    """Parse the args and create a pull request."""
    args = get_args()
    if args.push:
        push_branch()

    create_pull_request(args.title, args.body, args.base, args.recips)

if __name__ == '__main__':
    main()
