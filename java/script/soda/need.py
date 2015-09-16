import abc
from .structure import *
from .feedback import *
#from .log import *
import sys

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
        return text.replace(str(self._pattern), str(self._value))


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
for arg in sys.argv[1:]:
    if '=' in arg:
        parts = arg.split('=')
        var = aString(parts[0])
        var.value = parts[1]
        _variables[parts[0]] = var
        print(info(var))
    else:
        print(warn('Syntax error in argument: %s' % arg))

class Need(Doable):
    def __init__(self, variable):
        self._variable = variable


    def _do(self):
        global _variables
        if self._variable._name in _variables:
            print(info(_variables[self._variable._name]))
        else:
            print(info("Variable '%s' is undefined." % self._variable._name))
            self._variable.value = input(ask("Please specify the value of '%s'!\n" % self._variable._name))
            _variables[self._variable._name] = (self._variable)

class SetVariable(Doable):
    def __init__(self, variable, value):
        self._variable = variable
        self._value = value

    def _do(self):
        global _variables
        self._variable.value = self._value
        _variables[self._variable._name] = (self._variable)

class CleverString(str):
    def __init__(self, value):
        self._value = str(value)

    @property
    def value(self):
        global _variables
#        caller = caller_name(2)
#        if '__init__' in caller:
#            raise RuntimeError("Do not resolve CleverString in constructors. If you do not understand why, just do not do it!")
        processed = self._value
        #TODO: check substitution, inf. loop at unknown var
        while '${' in processed:
            for name in _variables:
                variable = _variables[name]
                processed = variable.substitute(processed)
            print(info('resolved as: ' + processed))
        return processed
