from .feedback import *
from .structure import *
from .need import *
from .filetweak import *
import glob2

class GlobPattern:
    AllChildDirectory = '*/'
    AllSubDirectory = '**/'

class FromDirectory:
    def __init__(self, folder):
        self._folder = folder

    def get(self, pattern):
        _folder = CleverString(self._folder).value
        _pattern = CleverString(pattern).value
        for item in glob2.iglob(str(f(_folder)/_pattern)):
            yield item

print(info("%s are loaded." % as_proper("Filesystem utils")))