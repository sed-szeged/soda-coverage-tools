from .feedback import *
from .filesystem import *
from .soda import *
from .call import *
from .structure import *
from .filetweak import *
from .commonutil import *

class MutantCode:
    def __init__(self, source_path, list_path=None):
        self.source_path = source_path
        if not list_path:
            list_path = str(f(source_path)/'..')
        with open(str(f(list_path)/'mutants.list.csv'), 'r') as hid:
            for line in hid:
                entry = [item.strip() for item in line.split(';')]
                if source_path == entry[-1].strip() + '/':
                    self.entry = entry
                    break
            else:
                pdb.set_trace()

    def generateTestResults(self, output_path):
        _source_path = CleverString(self.source_path).value
        return Phase('generate test results for mutant',
            CallMaven(['clean', 'test'], ['soda-dump-test-results']).From(_source_path),
            CollectFiles(self.source_path, f('target')/'jacoco'/'0'/'TestResults.r0', f(output_path)),
        )

def _getMutants(self):
    for mutant_source in self.get(GlobPattern.AllChildDirectory):
        yield MutantCode(mutant_source)

FromDirectory.getMutants = _getMutants

class GenerateTestResultForMutant(Doable):
    def __init__(self, mutant, output_path, list_path):
        self._mutant = mutant
        self._output_path = output_path
        self._list_path = list_path

    def _do(self, *args, **kvargs):
        _source_path = CleverString(self._mutant.source_path).value
        print(info("Generate test results for mutants at '%s'" % as_proper(_source_path)))
        self._mutant.generateTestResults(self._output_path).do()
        _output_path = CleverString(self._output_path).value
        _list_path = CleverString(self._list_path).value
        with open(str(f(_list_path)/'mutants.list.csv'), 'a') as hid:
            hid.write('%s;%s\n' % (';'.join(self._mutant.entry), _output_path))

class GenerateTestResultForMutants(Phase):
    def __init__(self, name, output_path, mutants):
        super().__init__(name)
        self._mutants = list(mutants)
        self._output_path = output_path
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

    def _do(self):
        _output_path = CleverString(self._output_path).value
        _from = None
        _to = None
        _by = None
        if self._from:
            _from = int(CleverString(self._from).value)
        if self._to:
            _to = int(CleverString(self._to).value)
        if self._by:
            _by = int(CleverString(self._by).value)
        _mutants = list(self._mutants[_from:_to:_by])
        self._steps = []
        for index, mutant in enumerate(_mutants):
            real_index = noneToDef(self._from) + (index * noneToDef(self._by)) + 1
            step = GenerateTestResultForMutant(mutant, f(_output_path)/'data'/str(real_index), _output_path)
            self._steps.append(step)
        super()._do()

print(info("%s is loaded." % as_proper("Mutant handling")))