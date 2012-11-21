#!/usr/bin/env python
import os
import os.path
import subprocess
import sys
import tempfile
import urllib2

# Welcome message
install_message = '''
 ____              _         ____ _ _
/ ___| _ __   __ _| | _____ / ___(_) |_
\___ \| '_ \ / _' | |/ / _ \ |  _| | __|
 ___) | | | | (_| |   <  __/ |_| | | |_ 
|____/|_| |_|\__,_|_|\_\___|\____|_|\__|

This installer configures your development environment
to work with the SnakeGit set of tools.  SnakeGit
integrates standard development and build workflows 
with git for a (hopefully) more consistent development
experience.
'''
print install_message
should_install = raw_input("Would you like to continue with installing [y]? ")
if should_install.lower() not in ['y', 'yes', 'yeah', 'yea', '']:
  print "Sorry to hear it"
  sys.exit(0)

#Now that that is taken care of, install snakegit
default_path = os.environ.get("SNAKEGIT_HOME", os.path.expanduser('~/.snakegit'))
prompt = "Where do you want to install SnakeGit [{0}] ?".format(default_path)
home = raw_input(prompt)
if home is None or home == '':
  home = default_path
if not os.path.exists(home):
  print "Installing SnakeGit"
  subprocess.call("git clone https://github.com/NarrativeScience/snakegit.git {0} 2>&1 | tee /tmp/snakegit_install.log".format(home), shell=True)

home = os.environ.get('SNAKEGIT_HOME', os.path.expanduser('~/.snakegit'))
if not os.path.exists(os.path.join(home, 'bin', 'python')):
  virtualenv_src = urllib2.urlopen('https://raw.github.com/pypa/virtualenv/master/virtualenv.py').read()
  fd, path = tempfile.mkstemp()
  os.write(fd, virtualenv_src)
  os.close(fd)
  if os.path.exists('/tmp/virtualenv.py'):
    os.remove('/tmp/virtualenv.py')

  subprocess.call("python {0} --distribute {1}".format(path, home), shell=True)
  os.remove(path)
current_dir = os.getcwd()
os.chdir(home)
cmd = '{0}/bin/pip install --find-links=file://{1} -r requirements.txt'.format(home, os.path.join(home, 'vendor', 'cache'))
subprocess.call(cmd, shell=True)
subprocess.call('{0}/bin/python setup.py install'.format(home), shell=True)
os.chdir(current_dir)
executable = os.path.join(home, 'bin', 'python')
script = os.path.join(home, 'src', 'snakes', 'config.py')
cmd = [
  "{0}/bin/python".format(home),
  script,
  "-i"
]
subprocess.call(cmd)
