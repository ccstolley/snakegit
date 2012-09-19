import clint.textui
import subprocess
import signal
import sys


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


