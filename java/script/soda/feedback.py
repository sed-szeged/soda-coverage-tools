from termcolor import colored
import sys, re
import threading, time
import pdb

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

def as_sample(text):
    return colored(text, 'cyan')

def info(text):
    return tagged(text, colored('i','white', 'on_green'), delimiter=' ')

def error(text):
    return tagged(text, colored('!','white', 'on_red'), delimiter='!')


def warn(text):
    return tagged(text, colored('w','white', 'on_magenta'))


def ask(text):
    return tagged(text, colored('?', 'white', 'on_cyan'), delimiter='?')

class ProgressBar:
    def __init__(self, width=100, x=0, y=0, name='progress'):
        self._x = x
        self._y = y
        self._width = width
        self.name = name
        self.value = 0

    def put(self, x, y):
        self._x = x
        self._y = y

    def draw(self):
        text = "\033[s"
        text += "\033[%d;%df" % (self._y, self._x)
        currentValueWidth = int(self._width * self.value)
        text += ('%s %f\n[' % (colored(self.name, 'green'), self.value*100)) + ''.join([colored('=', 'green', 'on_green') for i in range(currentValueWidth)]) + ''.join([colored('-', 'white', 'on_white') for i in range(self._width - currentValueWidth)]) + ']'
        text += "\033[u"
        print(text, end='')

    def clear(self):
        text = "\033[s"
        text += "\033[%d;%df\033[K\033[%d;%df\033[K\033[%d;%df\033[K" % (self._y-1, self._x, self._y+1, self._x, self._y+2, self._x)
        text += "\033[%d;%df\033[K" % (self._y, self._x)
        text += "\033[u"
        print(text, end='')

bars = []
is_render = True

def renderProgress():
    global bars
    while is_render:
        y = 3
        for bar in bars:
            bar.put(0, y)
            bar.draw()
            y += 4
        time.sleep(.001)
        for bar in bars:
            bar.put
            bar.clear()

progressRender = threading.Thread(target=renderProgress, args=())
progressRender.daemon = True
progressRender.start()