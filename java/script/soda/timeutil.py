from .structure import *
from .need import *
from .feedback import *
import datetime, time

def timestamp(time=None):
    time = time or datetime.datetime.utcnow()
    return time.strftime("%d-%m-%Y_%H:%M:%S")

class Wait(Doable):
    def __init__(self, seconds):
        super().__init__()
        self._seconds = seconds

    def _do(self, *args, **kvargs):
        _seconds = CleverString(self._seconds).value
        print(warn("Waiting (doing nothing) for %s seconds." % as_sample(_seconds)))
        time.sleep(_seconds)

print(info("%s is loaded" % as_proper("Time utils")))