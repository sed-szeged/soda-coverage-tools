from .feedback import *
from .structure import *
from .need import *
import os
import re
import shutil

print(info(as_proper("File tweaking")+" features loaded."))

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

class Restore(Doable):
    def __init__(self, original_path):
        self._original_path = original_path

    def _do(self, *args, **kvargs):
        back_up = CleverString(self._original_path+".original").value
        true_name = CleverString(self._original_path).value
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