from soda import info, error, warn, ask
from soda import Phase, Call, Need, aString
from soda import test

for i in test():
    print("out %d" % i)

print(info("In 'Mission Control Technologies'"))
Phase('build',
    Need(aString('name')),
    Call('echo Hello ${name}!')
).do()