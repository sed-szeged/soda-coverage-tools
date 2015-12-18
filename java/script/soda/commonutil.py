import os

def noneToDef(value, default=0):
    if not value:
        return default
    return value

def eitherFile(*paths):
    for p in paths:
        if os.path.isfile(p):
            return p
    else:
        raise FileNotFoundError()