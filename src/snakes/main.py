#!/usr/bin/env python
import argparse
import pkg_resources

import snakes.util
import clint


def main():
  cmds = sorted([ str(script).split(" = ")[0] for script in pkg_resources.iter_entry_points(group="snake_scripts") ])

  epilog='''
  The following commands are currently available:

  {0}
  '''.format( "\n  ".join(cmds))
  
  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      epilog=epilog)
  args = parser.add_argument('command', metavar="command", type=str,
      help="Command to execute")
  args = parser.parse_args() 
  snakes.util.run_cmd(args.command)

if __name__ == "__main__":

  main()

