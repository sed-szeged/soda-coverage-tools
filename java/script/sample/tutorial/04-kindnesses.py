from soda import *

Phase('path assembling',
    SetVariable(aString('path'), f('/')/'home'/'geryxyz'),
    Call('ls -l ${path}')
).do()