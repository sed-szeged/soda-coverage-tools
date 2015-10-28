from .feedback import *
import re

def getIndent(text):
    return re.search(r'^(?P<tabs>\s*)', text).group('tabs')

print(info("%s is loaded." % as_proper('String utils')))