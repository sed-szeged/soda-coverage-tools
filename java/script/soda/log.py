import os
from .structure import *
from .need import *
from .feedback import *
import inspect
import builtins

def print(*args, **kvargs):
    global settings
    if settings.mode > FeedbackModes.silent:
        builtins.print(*args, **kvargs)

size_of = lambda f: os.path.getsize(f)

class LogFile(Doable):
    def __init__(self, target, action, logput):
        self._target = target
        self._action = action
        self._logput = logput

    def _do(self, *args, **kvargs):
        print(dir())
        _logput = CleverString(self._logput).value
        _target = CleverString(self._target).value
        with open(_logput, 'a') as log:
            log.write('%s, %s\n' % (_target, str(self._action(_target))))

def caller_name(skip=2):
    """Get a name of a caller in the format module.class.method

       `skip` specifies how many levels of stack to skip while getting caller
       name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

       An empty string is returned if skipped levels exceed stack height
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
      return ''
    parentframe = stack[start][0]

    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append( codename ) # function or a method
    del parentframe
    return ".".join(name)

print(info(as_proper("Feadback") + " feautres are loaded."))
