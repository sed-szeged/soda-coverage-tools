import git #http://gitpython.readthedocs.org/en/latest/tutorial.html
import abc

class SCM(object, metaclass=abc.ABCMeta)
    def __init__(self, repo):
        self._repo = repo

    @abc.abstractmethod
    def checkout(self, path, version):
        pass

class From(object):
    def __init__(self, scm):
        self._scm = scm


    def 