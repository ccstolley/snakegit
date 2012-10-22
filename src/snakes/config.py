#!/usr/bin/env python

import argparse
import getpass
import json
import os
import os.path
import urllib2
import tempfile
import shutil
import subprocess
import sys

import clint.textui.colored
import git
import requests
import snakes.util


GH_AUTH_URL = 'https://api.github.com/authorizations'

GH_REQUEST_DATA = {
    "scopes": ["repo", "gist"],
    "note": "SnakeGit tools"
    }

def prompt_boolean(text, default_):
    text_default = "%s [%s]? " % (text.rstrip('?'), 'y' if default_ else 'n')
    text_colored = clint.textui.colored.yellow(text_default)
    response = raw_input(text_colored).strip()
    if response is None or len(response) == 0:
        return default_
    return response.lower() in ['y', 'yes', 'yea', 'yeah']

def register_github_interactive(user):
    '''Prompt for username and pass, return github (auth token, url) tuple'''
    while True:
        user = raw_input("What is your github username [{0}]? ".format(user))
        password = getpass.getpass("What is your github password? ")
        result = requests.post(GH_AUTH_URL, data=json.dumps(GH_REQUEST_DATA),
                               auth=(user, password))
        data = result.json
        message = data.get('message', None)
        if message is not None:
            prompt = 'Github login failed: %s\nRetry?' % message
            if prompt_boolean(prompt, True):
                continue
            sys.exit(1)
        try:
            return (data['token'], data['url'])
        except KeyError:
            prompt = 'Incomplete reply from Github: %s\nRetry?' % data
            if not prompt_boolean(prompt, True):
                sys.exit(1)

def register_github(reader, writer, user=''):
    print "Register github"
    (token, url) = register_github_interactive(user)
    if not reader.has_section('github'):
        writer.add_section('github')
    writer.set('github', 'user', user)
    writer.set('github', 'token', token)
    writer.set('github', 'url', url)

def register_pypi(reader, writer):
    print "Register with Pypi"
    url = 'https://repo.n-s.us/token'
    user = raw_input('What is your PyPi username? ')
    password = getpass.getpass("What is your PyPi password?")
    result = requests.post(url, auth=(user, password), verify=False).json
    if not reader.has_section('pypi'):
        writer.add_section('pypi')
    writer.set('pypi', 'user', result['uid'])
    writer.set('pypi', 'key', result['key'])


def main():
    """docstring for main"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interactive',
            action='store_true', default=False,
            help="Ask interactive questions")
    args = parser.parse_args()
    home = os.environ.get("SNAKEGIT_HOME", os.path.expanduser('~/.snakegit'))
    repo = git.Repo(home)
    reader = repo.config_reader(config_level='global')
    writer = repo.config_writer(config_level='global')
    if args.interactive:
        if not reader.has_section('alias'):
            writer.add_section('alias')
        writer.set('alias', 'snake', '! {0}/bin/snake'.format(home))
        writer.write()

        if reader.has_option('github', 'url'):
            if prompt_boolean('''You already seem to have github configured.
Do you want to reset it?''', False):
                register_github(reader, writer, reader.get('github', 'user'))
        else:
            register_github(reader, writer)
        if reader.has_option('pypi', 'user'):
            if prompt_boolean('''You already seem to have pypi configured.
Do you want to reset it?''', False):
                register_pypi(reader, writer)
        else:
            register_pypi(reader, writer)

if __name__ == '__main__':
    main()
