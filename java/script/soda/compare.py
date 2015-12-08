from .structure import *
from .feedback import *
from .need import *
import glob
import subprocess as sp #https://docs.python.org/3.4/library/subprocess.html
import pdb

class TestResultDelta:
    def __init__(self, name, *states):
        self.name = name
        self.states = states

    def writeTo(self, output):
        output.write(self.name)
        for state in self.states:
            output.write(', %s' % state)
        output.write('\n')

class ForwardCompareTestResult(Doable):
    def __init__(self, testresult0, testresult1, delta_path):
        self._testresult0 = testresult0
        self._testresult1 = testresult1
        self._delta_path = delta_path

    def _do(self, *args, **kvargs):
        _testresult0 = CleverString(self._testresult0).value
        _testresult1 = CleverString(self._testresult1).value
        _delta_path = CleverString(self._delta_path).value
        deltas = []
        with open(_testresult0) as res0, open(_testresult1) as res1:
            count0 = sum(1 for _ in res0)
            count1 = sum(1 for _ in res1)
            if count0 != count1:
                print(warn("mismatching number of tests: %s != %s" % (as_sample(count0), count1)))
            for entry0 in res0:
                name0, status0 = self._splitEntry(entry0)
                for entry1 in res1:
                    name1, status1 = self._splitEntry(entry1)
                    if name0 == name1:
                        if status0 != status1:
                            deltas.append(TestResultDelta(name0, status0, status1))
                        break
                else:
                    deltas.append(TestResultDelta(name0, status0, 'MISSING'))
        print(info("writing %s delta into %s" % (as_sample(len(deltas)),as_proper(_delta_path))))
        with open(_delta_path, 'w') as output:
            for delta in deltas:
                delta.writeTo(output)

    def _splitEntry(self, entry):
        parts = entry.strip().split(': ')
        return parts[1], parts[0]


print(info("%s are loaded." % as_proper("Comparation utils")))