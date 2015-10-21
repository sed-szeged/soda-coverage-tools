from .structure import *
from .feedback import *
from .need import *
import glob
import subprocess as sp #https://docs.python.org/3.4/library/subprocess.html
import pdb

class IsDeterministic(Doable):
    def __init__(self, path_pattern):
        self._path_pattern = path_pattern

    def _do(self, *args, **kvargs):
        _path_pattern = CleverString(self._path_pattern).value
        files = glob.glob(_path_pattern)
        for file1 in files:
            for file2 in files:
                Need(aString('soda_coverageComparator_path'))._do(*args, **kvargs)
                command = CleverString('${soda_coverageComparator_path} -c %s %s' % (file1, file2)).value
                output = sp.check_output(command, shell=True, *args, **kvargs)
                pdb.set_trace()

print(info("%s are loaded." % as_proper("Comparation utils")))