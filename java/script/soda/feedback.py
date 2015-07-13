_indentlevel = 0

def indent():
    global _indentlevel
    _indentlevel += 1

def undent():
    global _indentlevel
    _indentlevel -= 1

def tagged(text, tag, delimiter='|'):
    prefix = ''
    for i in range(_indentlevel):
        prefix += '%s  ' % delimiter
    return '[%s] %s%s' % (tag, prefix, text)


def info(text):
    return tagged(text, 'i', delimiter=' ')


def error(text):
    return tagged(text, '!', delimiter='!')


def warn(text):
    return tagged(text, 'w')


def ask(text):
    return tagged(text, '?', delimiter='?')