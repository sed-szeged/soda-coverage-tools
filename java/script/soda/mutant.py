from .feedback import *
from .filesystem import *
from .soda import *
from .call import *
from .structure import *

class MutantCode:
    def __init__(self, source_path):
        self.source_path = source_path

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
    def __init__(self, mutant, output_path):
        self._mutant = mutant
        self._output_path = output_path

    def _do(self, *args, **kvargs):
        self._mutant.generateTestResults(self._output_path).do()

print(info("%s is loaded." % as_proper("Mutant handling")))