from soda import *

Phase('main',                       #name of phase
    Phase('greating',               #subphase                \
        Need(aString('name')),      #   paramter declaration |
        Call('echo Hello ${name}!') #   paramter usage       |-> declaration of steps
    ),                              #                        |
    Call('echo end'),                #                        /
    LogFile('log.txt', size_of, '01-basic_structure.py')
).do()                              #execution of phase