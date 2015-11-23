from .feedback import *
from .filesystem import *
from .soda import *
from .call import *
from .structure import *
from .filetweak import *
from .commonutil import *
from .paralellutil import *
import os

class MutantCode:
    def __init__(self, entry):
        self.entry = [item.strip() for item in entry.split(';')]
        self.key = self.entry[3]
        self.source_path = self.entry[-1]

    def generateTestResults(self, output_path):
        _source_path = CleverString(self.source_path).value
        return Phase('generate test results for mutant',
            CallMaven(['clean', 'test'], ['soda-dump-test-results']).From(_source_path),
            CollectFiles(self.source_path, f('target')/'jacoco'/'0'/'TestResults.r0', f(output_path)),
        )

class GenerateTestResultForMutant(Doable):
    def __init__(self, mutant, output_path, list_path):
        self._mutant = mutant
        self._output_path = output_path
        self._list_path = list_path

    def _do(self, *args, **kvargs):
        _source_path = CleverString(self._mutant.source_path).value
        print(info("Generate test results for mutants at '%s'" % as_proper(_source_path)))
        _output_path = CleverString(self._output_path).value
        self._mutant.generateTestResults(_output_path).do()
        if not os.listdir(_output_path):
            DeleteFolder(_output_path).do()
        _list_path = CleverString(self._list_path).value
        with open(str(f(_list_path)/'mutants.list.csv'), 'a') as hid:
            hid.write('%s;%s\n' % (';'.join(self._mutant.entry), _output_path))

class GenerateTestResultForMutants(Phase):
    def __init__(self, name, output_path, list_path):
        super().__init__(name)
        self.mutants = []
        self._output_path = output_path
        self._list_path = list_path
        self._from = None
        self._to = None
        self._by = None

    def fromMutant(self, index):
        self._from = index
        return self

    def to(self, index):
        self._to = index
        return self

    def by(self, index):
        self._by = index
        return self

    def _preDo(self):
        _output_path = CleverString(self._output_path).value
        _list_path = CleverString(self._list_path).value

        self.loadMutants(_list_path)
        self.generateRealIndexes()
        _by, _from, _to = self.processSliceParameters()
        self.generateSteps(_by, _from, _output_path, _to)

    def generateSteps(self, _by, _from, _output_path, _to):
        self._steps = []
        for mutant in self.mutants[_from:_to:_by]:
            print(info("Creating step for mutant '%s'" % as_proper(mutant.key)))
            if not hasattr(mutant, 'real_index'):
                pdb.set_trace()
            step = GenerateTestResultForMutant(mutant, f(_output_path) / 'data' / str(mutant.real_index), _output_path)
            self._steps.append(step)

    def processSliceParameters(self):
        _from = None
        _to = None
        _by = None
        if self._from:
            _from = int(CleverString(self._from).value)
            print(info("generate test results from %s" % as_sample(_from)))
        if self._to:
            _to = int(CleverString(self._to).value)
            print(info("generate test results to %s" % as_sample(_to)))
        if self._by:
            _by = int(CleverString(self._by).value)
            print(info("generate test results for every %s" % as_sample(_by)))
        return _by, _from, _to

    def generateRealIndexes(self):
        real_index = 1
        for mutant in self.mutants:
            mutant.real_index = real_index
            real_index += 1

    def loadMutants(self, _list_path):
        with open(_list_path, 'r') as list_of_mutants:
            for line in list_of_mutants:
                self.mutants.append(MutantCode(line.strip()))
        self.mutants = sorted(self.mutants, key=lambda m: m.key)
        print(info("%d mutants were loaded from '%s'" % (len(self.mutants), as_proper(_list_path))))

    def _do(self):
        self._preDo()
        super()._do()

developers_of_soda = ['gergo_balogh', 'david_havas', 'david_tengeri', 'bela_vancsics']
fruits = ['apple', 'cherry', 'apricot', 'avocado', 'banana', 'clementine', 'orange', 'grape']

class ParalellGenerateTestResultForMutants(GenerateTestResultForMutants):
    def __init__(self, name, output_path, list_path, name_of_workers=tuple('gery')):
        super().__init__(name, output_path, list_path)
        self._name_of_workers = name_of_workers

    def _do(self):
        self._preDo()
        _name_of_workers = [CleverString(name).value for name in self._name_of_workers]
        pool = ThreadPool(name_of_workers=_name_of_workers)
        indentOff()
        for index, step in enumerate(self._steps):
            print(info("Add step#%s to queue." % as_proper(index)))
            pool.add_task(step.do)
        pool.wait_completion()
        indentOn()

print(info("%s is loaded." % as_proper("Mutant handling")))