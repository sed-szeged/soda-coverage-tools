import git #http://gitpython.readthedocs.org/en/latest/tutorial.html
import abc
import shutil
from .structure import *
from .feedback import *
from .need import *

print(info(as_proper("Source control")+" support is loaded."))

class SCM(object, metaclass=abc.ABCMeta):
    def __init__(self, repo):
        self._repo = repo

    @property
    def repo(self):
        return CleverString(self._repo).value

    @abc.abstractmethod
    def checkout(self, path, version):
        pass

    @abc.abstractmethod
    def all(self, path, version):
        pass

    @abc.abstractmethod
    def last(self, path, version, n):
        pass
        
    @abc.abstractmethod
    def between(self, path, version, after, before):
        pass

class From(Doable):
    def __init__(self, scm):
        self._scm = scm

    def to(self, path):
        self._path = path
        return self
        
    def checkout(self, version = None):
        self._version = version
        return self

    def all(self):
        print(info("Iterating through repository versions."))
        path = CleverString(self._path).value
        version = CleverString(self._version).value
        global bars
        bar = ProgressBar(name='checkout from %s' % self._scm.repo)
        bar.value = 0
        bars.append(bar)
        commits = list(self._scm.all(path, version))
        count = len(commits)
        i = 0
        for commit in commits:
            print(info("Checkout to version: %s" % (as_proper(commit))))
            bar.value = i / count
            i += 1
            yield commit
        bars.remove(bar)
            
    def last(self, n = 1):
        print(info("Iterating through last %s repository versions." % (as_proper(n))))
        path = CleverString(self._path).value
        version = CleverString(self._version).value
        for commit in self._scm.last(path, version, n):
            print(info("Checkout to version: %s" % (as_proper(commit))))
            yield commit
            
    def between(self, after, before):
        _after = CleverString(after).value
        _before = CleverString(before).value
        print(info("Iterating through repository versions between %s and %s." % (as_proper(_after), as_proper(_before))))
        path = CleverString(self._path).value
        version = CleverString(self._version).value
        global bars
        bar = ProgressBar(name='checkout from %s' % self._scm.repo)
        bar.value = 0
        bars.append(bar)
        #TODO remove list cast!
        commits = self._scm.between(path, version, _after, _before)
        count = len(self._scm.getCommits(self._scm._repoObject.git, after = after, before = before))
        i = 0
        for commit in commits:
            print(info("Checkout to version: %s" % (as_proper(commit))))
            bar.value = i / count
            i += 1
            yield commit
        bars.remove(bar)

    def _do(self, *args, **kvargs):
        try:
            path = CleverString(self._path).value
            repo = CleverString(self._scm.repo).value
            version = CleverString(self._version).value
            self._scm.checkout(path, version)
            print(info("Repository cloned from %s to %s" % (as_proper(repo),as_proper(path))))
            if self._version:
                print(info("Version: %s" % (as_proper(version))))
        except:
            print(error("Failed to clone repository from %s" % (as_proper(repo))))

class GitRepo(SCM):
    def __init__(self, repo):
        SCM.__init__(self, repo)

    def checkout(self, path, commit):
        self.clone(path)
        if commit:
            self._checkout(commit)
            
    def _checkout(self, commit):
        print("futsz paraszt?")
        self._repoObject.git.checkout(commit)

    def clone(self, path):
        repo = CleverString(self._repo).value
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass
        self._repoObject = git.Repo.clone_from(repo, path)

    def all(self, path, version):
        self.checkout(path, version)
        commits = self.getCommits(self._repoObject.git)
        return self.iterateCommits(commits)

    def last(self, path, version, n):
        self.checkout(path, version)
        commits = self.getCommits(self._repoObject.git, n)
        return self.iterateCommits(commits)

    def between(self, path, version, after, before):
        self.checkout(path, version)
        commits = self.getCommits(self._repoObject.git, after = after, before = before)
        return self.iterateCommits(commits)

    def iterateCommits(self, commits):
        for commit in commits:
            print(commit)
            self._checkout(commit)
            self._repoObject.git.clean('-xfd')
            yield commit
            
    def getCommits(self, git, n = None, after = None, before = None):
        params = []
        params.append('--pretty=format:"%H"')
        if n:
            params.append('-n ' + str(n))
        if after:
            params.append('--after=' + after)
        if before:
            params.append('--before=' + before)
        info = git.log(params)
        commits = info.strip('"').split('"\n"')
#        print(commits)
        return commits