import abc
from .structure import *
from .feedback import *

print(info(as_proper("Needs")+" features are loaded."))

class Variable(object, metaclass=abc.ABCMeta):
    def __init__(self, name, pattern=None):
        self._name = name
        if pattern:
            self._pattern = pattern
        else:
            self._pattern = '${%s}' % name


    @abc.abstractproperty
    def value(self):
        pass


    def substitute(self, text):
        return text.replace(self._pattern, self._value)


    def __str__(self):
        return "'%s' (%s) = '%s' of '%s'" % (self._name, self._pattern, self.value, self.__class__.__name__)


class aString(Variable):
    def __init__(self, name, pattern=None):
        super(aString, self).__init__(name, pattern)
        self._value = ''


    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, value):
        self._value = value


_variables = {}


class Need(Doable):
    def __init__(self, variable):
        self._variable = variable


    def _do(self):
        global _variables
        if self._variable._name in _variables:
            print(info(self._variable))
        else:
            print(info("Variable '%s' is undefined." % self._variable._name))
            self._variable.value = input(ask("Please specify the value of '%s'!\n" % self._variable._name))
            _variables[self._variable._name] = (self._variable)


class CleverString(str):
    def __init__(self, value):
        self._value = str(value)


    @property
    def value(self):
        global _variables
        processed = self._value
        for name in _variables:
            variable = _variables[name]
            processed = variable.substitute(processed)
        return processed
    
