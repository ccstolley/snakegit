#!/usr/bin/env python

import snakes.util
import clint.textui
import ConfigParser
import argparse

def main():
  """docstring for main"""
  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument('-u', '--micro',
      action="store_true",
      help="bump the micro version")
  group.add_argument('-m', '--minor',
      action="store_true",
      help="bump the minor version")
  group.add_argument('-M', '--major',
      action="store_true",
      help="bump the major version")
  parser.add_argument("-s", "--snapshot",
      action="store_true",
      help="This is a snapshot version")
  args = parser.parse_args()
  config = ConfigParser.RawConfigParser()
  config.read("./snake.cfg")
  current_version = config.get('release', 'version')
  major, minor, micro = current_version.split('.')
  micro = micro.replace('-SNAPSHOT', '') 
  if args.micro:
    micro = int(micro) + 1
  if args.minor:
    minor = int(minor) + 1
  if args.major:
    major = int(major) + 1
  version = "{0}.{1}.{2}".format(major, minor, micro)
  if args.snapshot:
    version = "{0}-SNAPSHOT".format(version)

  prompt = "You are about to bump the version from {0} to {1}.".format(current_version, version)

  if snakes.util.confirm(prompt):
    config.set('release', 'version', version)
    with open('./snake.cfg', 'w') as f:
      config.write(f)
    print clint.textui.colored.blue("Version updated.")
  else:
    print clint.textui.colored.yellow("Not bumping version.")

if __name__ == '__main__':
  main()
