from .need import *
from .feedback import *
from .structure import *
import os
import re
import shutil
import glob2

print(info(as_proper("File tweaking")+" features loaded."))

def pj(*args):
    return os.path.join(*[str(a) for a in args])

def folder(*name):
    cpath = CleverPath()
    cpath.extend(name)
    return cpath

f = folder

class CleverPath(list):
    def __str__(self):
        return os.path.join(*[str(a) for a in self])

    def go(self, name):
        _new = CleverPath()
        _new.extend(self[:])
        if name is list:
            _new.extend(name)
        else:
            _new.append(name)
        return _new

    def __truediv__(self, other):
        return self.go(other)


def insert(what, into, where):
    with open(into, 'r') as f:
        contents = f.readlines()
    index = None
    line = None
    for i in range(len(contents)):
        if re.search(where, contents[i]):
            line = contents[i]
            index = i
            break
    else:
        raise Exception("Pattern not found in '%s' file" % as_proper(into))
    contents.insert(index, what)
    print(info("Insert into '%s' file before: '%s'" % (into, line.strip())))
    with open(into+".tmp", 'w') as f:
        f.write("".join(contents))
    os.rename(into, into+".original")
    os.rename(into+".tmp", into)

def backup(what):
    dst = what + '.original'
    if os.path.exists(dst):
        return
    shutil.copy(what, dst)

def collectFilePaths(dirName, fileName):
    paths = []
    for root, dirs, files in os.walk(dirName):
        for name in files:
            if fileName == name:
                paths.append(os.path.join(root, name))
    return paths

class Restore(Doable):
    def __init__(self, path, fileName='pom.xml'):
        self._path = path
        self._fileName = fileName

    def _do(self, *args, **kvargs):
        self._paths = collectFilePaths(CleverString(self._path).value, self._fileName)
        for path in self._paths:
            back_up = CleverString(str(path)+".original").value
            true_name = CleverString(path).value
            if os.path.isfile(back_up):
                os.rename(back_up, true_name)
                print(info("%s is restored from %s." % (as_proper(true_name), as_proper(back_up))))
            else:
                print(info("Missing back-up for %s, looking for %s." %(as_proper(true_name), as_proper(back_up))))

class Copy(Doable):
    def __init__(self, from_path, to_path):
        self._from_path = from_path
        self._to_path = to_path

    def _do(self, *args, **kvargs):
        from_path = CleverString(self._from_path).value
        to_path = CleverString(self._to_path).value
        if os.path.isfile(from_path):
            print(info("Copy file %s to %s." % (as_proper(from_path), as_proper(to_path))))
            to_dir = os.path.dirname(to_path)
            if not os.path.exists(to_dir):
                os.makedirs(to_dir)
            shutil.copy(from_path, to_path)
        elif os.path.isdir(from_path):
            print(info("Copy directory tree %s to %s." % (as_proper(from_path), as_proper(to_path))))
            try:
                shutil.rmtree(to_path)
            except FileNotFoundError:
                pass
            shutil.copytree(from_path, to_path)
        else:
            print(error("%s is neither a file nor directory." % as_proper(from_path)))

class CopyMatching(Doable):
    def __init__(self, from_path, to_path, pattern, preserve_relative_path=True):
        self._from_path = from_path
        self._to_path = to_path
        self._pattern = pattern
        self._preserve_relative_path = preserve_relative_path

    def _do(self, *args, **kvargs):
        from_path = CleverString(self._from_path).value
        to_path = CleverString(self._to_path).value
        pattern = CleverString(self._pattern).value
        matching_files = glob2.glob(from_path + '/' + pattern)
        for p in matching_files:
            if self._preserve_relative_path:
                target_path = p.replace(from_path, to_path)
            else:
                target_path = f(to_path)/os.path.basename(p)
            Copy(p, target_path).do()

class DeleteFolder(Doable):
    def __init__(self, folder):
        self._folder = folder

    def _do(self, *args, **kvargs):
        _folder = CleverString(self._folder).value
        print(info("Delete %s" % (as_proper(_folder))))
        try:
            shutil.rmtree(_folder)
        except FileNotFoundError:
            pass

class CollectFiles(Doable):
    def __init__(self, root, pattern, to_path):
        self._root = root
        self._pattern = str(pattern)
        self._to_path = to_path

    def _do(self, *args, **kvargs):
        root = CleverString(self._root).value
        pattern = self._pattern
        to_path = CleverString(self._to_path).value
        to_copy = []
        for top, dirs, files in os.walk(root):
            for f in files:
                path = os.path.join(top, f)
                if re.search(pattern, path):
                    to_copy.append(path)
                    print(info("%s is matching to %s" % (as_proper(path), as_proper(pattern))))
        try:
            shutil.rmtree(to_path)
        except FileNotFoundError:
            pass
        os.makedirs(to_path)
        for f in to_copy:
            prop_file = os.path.join(to_path, os.path.basename(f))
            if os.path.exists(prop_file): # append to an existing file if already exists
                with open(prop_file, 'a') as outfile:
                    with open(f) as infile:
                        for line in infile:
                            outfile.write(line)
            else:
                shutil.copy(f, to_path)
            print(info("Append %s to %s" % (as_proper(f),as_proper(to_path))))

# TODO remove concurrent implementations below after single.py is properly updated
class CollectFiles2(Doable): 
    def __init__(self, root, pattern, to_path):
        self._root = root
        self._pattern = pattern
        self._to_path = to_path

    def _do(self, *args, **kvargs):
        root = CleverString(self._root).value
        pattern = CleverString(self._pattern).value
        to_path = CleverString(self._to_path).value
        to_copy = glob2.glob(pattern)
        try:
            shutil.rmtree(to_path)
        except FileNotFoundError:
            pass
        for f in to_copy:
            shutil.copytree(f, to_path)
            print(info("Copy %s to %s" % (as_proper(f),as_proper(to_path))))
            
class MergeFiles(Doable):
    def __init__(self, outfile, *filenames):
        self._outfile = outfile
        self._filenames = filenames

    def _do(self, *args, **kvargs):
        outfile = CleverString(self._outfile).value
        filenames = self._filenames
        with open(outfile, 'w') as out:
            for f in filenames:
                with open(f) as infile:
                    for line in infile:
                        out.write(line)
                print(info("File %s merged into %s" % (as_proper(f),as_proper(outfile))))
        print(info("File merge completed. Result: %s" % (as_proper(outfile))))
        
class MergeFilesInDirectory(Doable):
    def __init__(self, outfile, dir):
        self._outfile = outfile
        self._dir = dir

    def _do(self, *args, **kvargs):
        outfile = self._outfile
        dir = CleverString(self._dir).value
        paths = []
        for top, dirs, files in os.walk(dir):
            for f in files:
                path = os.path.join(top, f)
                paths.append(os.path.join(top, f))
        MergeFiles(outfile, *paths).do()
        
class MergeMatchingFiles(Doable):
    def __init__(self, outfile, pattern):
        self._outfile = outfile
        self._pattern = pattern

    def _do(self, *args, **kvargs):
        outfile = self._outfile
        pattern = CleverString(self._pattern).value
        paths = glob2.glob(pattern)
        MergeFiles(outfile, *paths).do()
