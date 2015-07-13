import subprocess as sp #https://docs.python.org/3.4/library/subprocess.html
from .feedback import *
from .structure import *
from .need import *

class Call(Doable):
    def __init__(self, command, splitby=' '):
        self._command = command
        self._splitby = splitby


    def _do(self):
        sp.call(CleverString(self._command).value.split(self._splitby), shell=True)