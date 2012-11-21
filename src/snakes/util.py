from __future__ import absolute_import

import clint.textui
import subprocess
import signal
import sys


from re import match, I

def yn(prompt, default='y', batch=False):
    if default not in ['y', 'n']:
        default = 'y'

    # Let's build the prompt
    choicebox = '[Y/n]' if default == 'y' else '[y/N]' 
    prompt = prompt + ' ' + choicebox + ' ' 

    # If input is not a yes/no variant or empty
    # keep asking
    while True:
        # If batch option is True then auto reply 
        # with default input
        if not batch:
            input = raw_input(prompt).strip()
        else:
            print prompt
            input = ''
            # If input is empty default choice is assumed

        # so we return True
        if input == '':
            return True

        # Given 'yes' as input if default choice is y
        # then return True, False otherwise 
        if match('y(?:es)?', input, I):
            return True if default == 'y' else False

        # Given 'no' as input if default choice is n
        # then return True, False otherwise
        elif match('n(?:o)?', input, I):
            return True if default == 'n' else False

class Completer(object):

    def __init__(self, completions):
        self.completions = completions

    def complete(self, text, state):
        buffer = readline.get_line_buffer()
        line = readline.get_line_buffer().split()
        if not line or len(line) == 0:
            return [ p + ' ' for p in self.completions ][state]
        pkg = buffer.strip()
        results = [p + ' ' for p in self.completions if p.startswith(pkg)] + [None]
        return results[state]

YES_VALUES = ['yes', 'y', 'ye', '']

def confirm(prompt):
    print prompt
    response = raw_input(clint.textui.colored.yellow("Are you sure [Y]?"))
    if response.lower() in YES_VALUES:
        return True
    return False

def install_signal_handlers():
    def signal_handler(signal, frame):
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

def run_cmd(cmd):
    install_signal_handlers()
    return subprocess.call(cmd, shell=False)


