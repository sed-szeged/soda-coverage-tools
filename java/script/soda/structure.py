import abc
from .feedback import *

print(info(as_proper("Logical structure")+" is loaded."))

class Doable(object, metaclass=abc.ABCMeta):
    _name = ''

    @abc.abstractmethod
    def _do(self, *args, **kvargs):
        pass

    def do(self):
        if self._name:
            print(info("Do '%s' {" % self._name))
        else:
            print(info("Do '%s' {" % self.__class__.__name__))
        indent()
        self._do()
        undent()
        if self._name:
            print(info("} '%s' is done." % self._name))
        else:
            print(info("} '%s' is done." % self.__class__.__name__))
        return

class Phase(Doable):
    def __init__(self, name, *steps):
        self._name = name
        self._steps = steps

    @property
    def name(self):
        return self._name


    def _do(self):
        for i in range(len(self._steps)):
            step = self._steps[i]
            print(info("Do step#%d {" % i))
            indent()
            step.do()
            undent()
            print(info("} step#%d done." % i))
        pass
