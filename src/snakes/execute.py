"""
Execute a command in the context of a snake project
"""
import os
import subprocess
import sys

def main():
    """
    Run the supplied program in the snake context
    """
    if len(sys.argv) < 2:
        print "Usage"
        print ""
        print "snake exec <command>"
        return 1
    command = sys.argv[1:]
    path = os.environ['PATH']
    result = subprocess.call(command, 
            env={'PATH': 'vendor/python/bin:{0}'.format(path)})

    return result

if __name__ == '__main__':
    sys.exit(main())


