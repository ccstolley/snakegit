import sh
import os
import argparse
from snakes.util import yn


def main():
    """
    Clean the build environment and optionally remove the virtualenv.
    """
    rm = sh.rm # define rm 
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--environment', action="store_true",
            help="Remove the virtualenv as well")
    args = parser.parse_args()
    rm('-rf', 'build', 'dist', 'gearbox', 'gearbox_dist')
    if args.environment:
        if yn("This will remove your Virtualenv.  Rebuilding it might take a long time.  Are you sure you want to do this?"):
            if 'VIRTUALENV_HOME' in os.environ:
                venv = os.environ['VIRTUALENV_HOME']
            else:
                venv = 'vendor/python'
            rm('-rf', venv)

if __name__ == '__main__':
    main()
