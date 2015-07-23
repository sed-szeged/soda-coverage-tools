import subprocess as sp #https://docs.python.org/3.4/library/subprocess.html
from .feedback import *
from .structure import *
from .need import *

print(info(as_proper("Commandline call") + " features are loaded."))

class Call(Doable):
    def __init__(self, command, splitby=' '):
        self._command = command
        self._splitby = splitby

    def _do(self, *args, **kvargs):
        command = CleverString(self._command).value
        #command = CleverString(self._command).value.split(self._splitby)
        print(info('executing: %s' % command))
        sp.call(command, shell=True, *args, **kvargs)
