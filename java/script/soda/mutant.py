from .feedback import *
from .filesystem import *
from .soda import *
from .call import *
from types import *


class MutantCode:
    def __init__(self, source_path):
        self._source_path = source_path

    def generateTestResults(self, output_path):
        _source_path = CleverString(self._source_path).value
        return Phase('mutant live cycle',
            CallMaven(['clean', 'test'], ['soda-dump-test-results'], cwd=_source_path),
            CollectFiles(self._source_path, f('target')/'jacoco'/'0'/'TestResults.r0', f(output_path)/'raw-test-data'),
        )


def _getMutants(self):
    for mutant_source in self.get(GlobPattern.AllChildDirectory):
        yield MutantCode(mutant_source)

FromDirectory.getMutants = _getMutants

print(info("%s is loaded." % as_proper("Mutant handling")))