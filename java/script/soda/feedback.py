from termcolor import colored

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

def as_proper(name):
    return colored(name, 'yellow')

def info(text):
    return tagged(text, colored('i','white', 'on_green'), delimiter=' ')

def error(text):
    return tagged(text, colored('!','white', 'on_red'), delimiter='!')


def warn(text):
    return tagged(text, colored('w','white', 'on_magenta'))


def ask(text):
    return tagged(text, colored('?', 'white', 'on_cyan'), delimiter='?')

print(info(as_proper("Feadback") + " feautres are loaded."))
