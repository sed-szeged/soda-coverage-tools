from .feedback import *
from .filesystem import *
from .soda import *
from .call import *
from .structure import *
from .filetweak import *

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
        self._mutant.generateTestResults(self._output_path).do()
        _output_path = CleverString(self._output_path).value
        _list_path = CleverString(self._list_path).value
        with open(str(f(_list_path)/'mutants.list.csv'), 'a') as hid:
            hid.write('%s;%s\n' % (';'.join(self._mutant.entry), _output_path))

print(info("%s is loaded." % as_proper("Mutant handling")))