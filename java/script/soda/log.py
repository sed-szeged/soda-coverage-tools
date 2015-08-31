import os
from .structure import *
from .need import *

size_of = lambda f: os.path.getsize(f)

class LogFile(Doable):
    def __init__(self, target, action, logput):
        self._target = target
        self._action = action
        self._logput = logput

    def _do(self, *args, **kvargs):
        _logput = CleverString(self._logput).value
        _target = CleverString(self._target).value
        with open(_logput, 'a') as log:
            log.write('%s, %s\n' % (_target, str(self._action(_target))))

print(info(as_proper("Feadback") + " feautres are loaded."))
