from soda import *

print("\n"*3)

#primitive feedbacks
print(info("Some information about the execution of %s" % as_proper("The Script")))
print(ask("Need more information?"))
print(warn("I don't think it is good."))
print(error("No, it is defenetly wrong!"))

print("\n"*3)
pdb.set_trace()

#progressbar demo
Phase('külső',
    Phase('belső',
        Need(aString('0')),
        Need(aString('1')),
        Need(aString('2')),
        Need(aString('3')),
    ),
    Phase('másik',
        Need(aString('a')),
        Need(aString('b')),
        Need(aString('c')),
        Need(aString('d')),
    ),
    Need(aString('end'))
).do()