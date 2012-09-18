#!/usr/bin/env python

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


def register_github(reader, writer, user=''):
	print "Register github"
	request_data = {
				"scopes": ["repo", "gist"],
				"note": "SnakeGit tools"
				}
	url = 'https://api.github.com/authorizations'
	user = raw_input("What is your github username [{0}]? ".format(user))
	password = getpass.getpass("What is your github password? ")
	result = requests.post(url, data=json.dumps(request_data), auth=(user, password))

	data = result.json
	if not reader.has_section('github'):
		writer.add_section('github')
	writer.set('github', 'user', user)
	writer.set('github', 'token', data['token'])
	writer.set('github', 'url', data['url'])

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
	home = os.environ.get("SNAKEGIT_HOME", os.path.expanduser('~/.snakegit'))
	repo = git.Repo(home)
	reader = repo.config_reader(config_level='global')
	writer = repo.config_writer(config_level='global')
	if not reader.has_section('alias'):
		writer.add_section('alias')
	writer.set('alias', 'snake', '! {0}/bin/snake'.format(home))
	writer.write()

	if reader.has_option('github', 'url'):
		reset_github = clint.textui.colored.yellow('''
You already seem to have github configured.
Do you want to reset it [n]? ''')
		response = raw_input(reset_github)
		if response.strip().lower() in  ['y', 'yes', 'yea', 'yeah']:
			register_github(reader, writer, reader.get('github', 'user'))
	else:
		register_github(reader, writer)
	if reader.has_option('pypi', 'user'):
		reset_pypi = clint.textui.colored.yellow('''
You already seem to have pypi configured.
Do you want to reset it [n]? ''')
		response = raw_input(reset_pypi)
		if response.strip().lower() in  ['y', 'yes', 'yea', 'yeah']:
			register_pypi(reader, writer)
	else:
		register_pypi(reader, writer)

if __name__ == '__main__':
	main()
