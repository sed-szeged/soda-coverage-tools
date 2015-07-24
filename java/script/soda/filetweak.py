from .feedback import *
from .structure import *
from .need import *
import os
import re

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
