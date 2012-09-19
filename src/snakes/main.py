#!/usr/bin/env python
import os
import os.path
import pkg_resources
import sys

import snakes.util


def main():
    home = os.environ.get('SNAKEGIT_HOME', os.path.expanduser('~/.snakegit'))
    cmds = sorted([str(script).split(" = ")[0] for script in pkg_resources.iter_entry_points(group="snake_scripts")])

    epilog = '''
  The following commands are currently available:

  {0}
  '''.format("\n  ".join(cmds))

    args = sys.argv[1:]
    if args[0] == '-h':
        print epilog
    else:
        snakes.util.run_cmd(["{0}/bin/{1}".format(home, args[0]),] + args[1:])

if __name__ == "__main__":
    sys.exit(main())
