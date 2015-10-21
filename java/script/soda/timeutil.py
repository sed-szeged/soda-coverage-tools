from .structure import *
from .feedback import *
import datetime

def timestamp(time=None):
    time = time or datetime.datetime.utcnow()
    return time.strftime("%d-%m-%Y_%H:%M:%S")

print(info("%s is loaded" % as_proper("Time utils")))