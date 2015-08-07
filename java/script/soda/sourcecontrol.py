import git #http://gitpython.readthedocs.org/en/latest/tutorial.html
import abc
from .structure import *
from .feedback import *
from .need import *

print(info(as_proper("Source control")+" support is loaded."))

class SCM(object, metaclass=abc.ABCMeta):
    def __init__(self, repo):
        self._repo = repo

    @abc.abstractmethod
    def checkout(self, path, version):
        pass

class From(Doable):
    def __init__(self, scm):
        self._scm = scm

    def to(self, path):
        self._path = path
        return self

    def _do(self, *args, **kvargs):
        path = CleverString(self._path).value
        self._scm.checkout(path, "")

class GitRepo(SCM):
    def __init__(self, repo):
        SCM.__init__(self, repo)

    def checkout(self, path, version):
        self.clone(path)

    def clone(self, path):
        repo = CleverString(self._repo).value
        try:
            git.Repo.clone_from(repo, path)
            print(info("Repository cloned from %s to %s" % (as_proper(self._repo),as_proper(path))))
        except:
            print(error("Failed to clone repository from %s" % (as_proper(self._repo))))
            pass