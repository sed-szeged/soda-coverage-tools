from abc import abstractmethod
from abc import ABCMeta
import os
import hashlib
from collections import *

from .call import *
from .filetweak import *
from .paralellutil import *
from soda import CleverString, info, as_sample, as_proper
from .commonutil import *
from .mutation import *

isdir = os.path.isdir

class TestExecutorEngine:
    Jacoco = "jacoco"
    Clover = "clover"

class MutantCode:
    def __init__(self, entry, original_path=None, patch_path=None, relative_path_to_patch='', remove_mutantcode=False):
        self.entry = MutantListEntry(*[item.strip() for item in entry.split(';')])
        self.key = self.entry.key
        self.source_path = self.entry.path
        self._original_path = original_path
        self._patch_root = patch_path
        self._remove_mutantcode = remove_mutantcode
        self._relative_path_to_patch = relative_path_to_patch

    def initMutantCode(self):
        source_path = CleverString(self.source_path).value
        if not isdir(source_path) or not os.listdir(source_path):
            if not isdir(source_path):
                os.makedirs(source_path)
            print(warn("Missing source. Try to merge..."))
            original_path = CleverString(self._original_path).value
            patch_path = CleverString(self._patch_root).value
            if not (isdir(original_path) and isdir(patch_path)):
                print(error("%s or %s are invalid as original source and patch source" % (as_proper(original_path),as_proper(patch_path))))
                return
            MergeDirectory(original_path, patch_path, source_path, self._relative_path_to_patch).do()
            self._remove_mutantcode = True

    def generateTestResults(self, output_path, engine=TestExecutorEngine.Jacoco):
        self.initMutantCode()
        _source_path = CleverString(self.source_path).value
        steps = [CallMaven(['clean', 'test'], ['soda-dump-test-results']).From(_source_path)]
        if engine == TestExecutorEngine.Clover:
            steps.append(CollectFiles(self.source_path, f('target')/'clover'/'TestResults.r0', output_path))
        elif engine == TestExecutorEngine.Jacoco:
            steps.append(CollectFiles(self.source_path, f('target')/'jacoco'/'0'/'TestResults.r0', output_path))
        if self._remove_mutantcode:
            steps.append(DeleteFolder(self.source_path))
        return Phase('generate test results for mutant', *steps)

    def generateCoverageData(self, output_path):
        _source_path = CleverString(self.source_path).value
        return Phase('generate coverage data for mutant',
            CallMaven(goals=['clean', 'clover2:setup', 'test clover2:aggregate', 'clover2:clover'], properties=['maven.test.failure.ignore=true'], profiles=['soda-clover-coverage']).From(_source_path),
            CopyMatching(self.source_path, f(output_path)/'raw', f('target')/'clover'/'clover*', preserve_relative_path=False),
            ConvertCloverCoverageDataToSodaMatrix(output_path)
        )

MajorLogEntry = namedtuple('MajorLogEntry', ['id', 'operator', 'original_symbol', 'replacement_symbol', 'method', 'line_number', 'change'])

class MajorLogFilter(Filter):
    def __init__(self, log_path):
        self._entries = []
        print(warn("log_path=%s will be resolved at declaration time, the log file need to be exist before execution." % as_proper(log_path)))
        log_path = CleverString(log_path).value
        with open(log_path, 'r') as log_file:
            for line in log_file:
                parts = [part.strip() for part in line.strip().split(':', 6)]
                parts[-1] = Change(*[p.strip() for p in parts[-1].split('|==>')])
                self._entries.append(MajorLogEntry(*parts))

    def apply(self, data):
        self._mutant = MutantCode(data)

class MajorIdenticalChangeFilter(MajorLogFilter):
    def apply(self, data):
        super().apply(data)
        for entry in self._entries:
            if entry.id == self._mutant.entry.file and entry.change.before == entry.change.after:
                print(info('filter %s aka %s beacuse it is an identical change' % (as_proper(self._mutant.entry), as_proper(entry))))
                return False
        return True

class DictionariesToMutantList(Doable):
    def __init__(self, root, list_path, filter):
        self._root = root
        self._list_path = list_path
        self._filter = filter

    def _do(self, *args, **kvargs):
        root = CleverString(self._root).value
        list_path = CleverString(self._list_path).value
        with open(list_path, 'w') as list_file:
            for subdir in os.listdir(root):
                hashed = hashlib.md5()
                hashed.update(subdir.encode('utf-8'))
                hexdigest = hashed.hexdigest()
                entry = MutantListEntry(file=str(subdir), type='directory based', index='unknown', key=hexdigest, path=str(f(root)/subdir))
                if self._filter.apply(';'.join(entry)):
                    list_file.write('%s\n' % ';'.join(entry))
                    print(info("entry %s are created for directory %s" % (as_proper(entry), as_proper(subdir))))


class GenerateTestResultForMutant(Doable):
    def __init__(self, mutant, output_path, list_path, engine=TestExecutorEngine.Jacoco):
        self._mutant = mutant
        self._output_path = output_path
        self._list_path = list_path
        self._engine = engine

    def _do(self, *args, **kvargs):
        _source_path = CleverString(self._mutant.source_path).value
        print(info("Generate test results for mutants at '%s'" % as_proper(_source_path)))
        _output_path = CleverString(self._output_path).value
        if os.path.isdir(_output_path):
            print(warn("Skipping test result generation for %s: mutant folder already present." % as_sample(_output_path)))
        else:
            self._mutant.generateTestResults(_output_path, engine=self._engine).do()
        if os.path.isdir(_output_path) and not os.listdir(_output_path):
            DeleteFolder(_output_path).do()
        _list_path = CleverString(self._list_path).value
        with open(str(f(_list_path)/'mutants.list.csv'), 'a+') as hid:
            hid.write('%s;%s\n' % (';'.join(self._mutant.entry), _output_path))

class MutantsLoader(metaclass=ABCMeta):
    @abstractmethod
    def loadMutants(self):
        pass

class MutantsListLoader(MutantsLoader):
    def __init__(self, list_path):
        self._list_path = list_path

    def loadMutants(self):
        list_path = CleverString(self._list_path).value
        mutants = []
        with open(list_path, 'r') as list_of_mutants:
            for line in list_of_mutants:
                mutants.append(MutantCode(line.strip()))
        mutants = sorted(mutants, key=lambda m: m.key)
        print(info("%d mutants were loaded from '%s'" % (len(mutants), as_proper(list_path))))
        return mutants

class MutantsPatchLoader(MutantsLoader):
    def __init__(self, original_path, patch_root, merge_root, relative_path_to_patch=''):
        self._original_path = original_path
        self._patch_root = patch_root
        self._merge_root = merge_root
        self._relative_path_to_patch = relative_path_to_patch

    def loadMutants(self):
        original_path = CleverString(self._original_path).value
        patch_root = CleverString(self._patch_root).value
        merge_root = CleverString(self._merge_root).value
        relative_path_to_patch = CleverString(self._relative_path_to_patch).value
        mutants = []
        for patch_dir in os.listdir(patch_root):
            hashed = hashlib.md5()
            hashed.update(patch_dir.encode('utf-8'))
            hexdigest = hashed.hexdigest()
            entry = MutantListEntry(file=str(patch_dir), type='directory based', index='unknown', key=hexdigest, path=str(f(merge_root)/patch_dir))
            mutants.append(MutantCode(
                ';'.join(entry),
                original_path=original_path,
                patch_path=str(f(patch_root)/patch_dir),
                relative_path_to_patch=relative_path_to_patch))
        return mutants


class ProcessMutantsPhase(Phase, metaclass=ABCMeta):
    def __init__(self, name, output_path, mutants_loader):
        super().__init__(name)
        self.mutants = []
        self._output_path = output_path
        self._mutants_loader = mutants_loader
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

    @abstractmethod
    def generateSteps(self, _by, _from, _output_path, _to):
        pass

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

    def _preDo(self):
        _output_path = CleverString(self._output_path).value

        self.mutants = self._mutants_loader.loadMutants()
        self.generateRealIndexes()
        _by, _from, _to = self.processSliceParameters()
        self.generateSteps(_by, _from, _output_path, _to)

    def _do(self):
        self._preDo()
        super()._do()

class GenerateTestResultForMutants(ProcessMutantsPhase):
    def __init__(self, name, output_path, mutants_loader, engine=TestExecutorEngine.Jacoco):
        super().__init__(name, output_path, mutants_loader)
        self._engine = engine

    def generateSteps(self, _by, _from, _output_path, _to):
        self._steps = []
        for mutant in self.mutants[_from:_to:_by]:
            print(info("Creating step for mutant '%s'" % as_proper(mutant.key)))
            if not hasattr(mutant, 'real_index'):
                pdb.set_trace()
            step = GenerateTestResultForMutant(mutant, f(_output_path) / 'data' / str(mutant.real_index), _output_path, engine=self._engine)
            self._steps.append(step)

developers_of_soda = ['gergo_balogh', 'david_havas', 'david_tengeri', 'bela_vancsics']
fruits = ['apple', 'cherry', 'apricot', 'avocado', 'banana', 'clementine', 'orange', 'grape']
valar = ['Aldaron', 'Araw', 'Aule', 'Beleguur', 'Belegurth', 'Beema', 'Elbereth', 'Este', 'Irmo', 'Yavanna']

class ParalellGenerateTestResultForMutants(GenerateTestResultForMutants):
    def __init__(self, name, output_path, mutants_loader, name_of_workers=tuple('gery')):
        super().__init__(name, output_path, mutants_loader)
        self._name_of_workers = name_of_workers

    def _do(self):
        self._preDo()
        _name_of_workers = [CleverString(name).value for name in self._name_of_workers]
        pool = ThreadPool(name_of_workers=_name_of_workers)
        indentOff()
        Call.enableDocker(mounts=['~/.m2:/root/.m2', ], image='maven:3-jdk-7')
        for index, step in enumerate(self._steps):
            print(info("Add step#%s to queue." % as_proper(index)))
            pool.add_task(step.do)
        pool.wait_completion()
        Call.disableDocker()
        indentOn()


class GenerateCoverageDataForMutant(Doable):
    def __init__(self, mutant, output_path, list_path):
        self._mutant = mutant
        self._output_path = output_path
        self._list_path = list_path

    def _do(self, *args, **kvargs):
        _source_path = CleverString(self._mutant.source_path).value
        print(info("Generate coverage data for mutants at '%s'" % as_proper(_source_path)))
        _output_path = CleverString(self._output_path).value
        if os.path.isdir(_output_path):
            print(warn("Skipping coverage data generation for %s: mutant folder already present." % as_sample(_output_path)))
        else:
            self._mutant.generateCoverageData(_output_path).do()
        if not os.path.isdir(_output_path):
            os.makedirs(_output_path)
        if not os.listdir(_output_path):
            DeleteFolder(_output_path).do()
        _list_path = CleverString(self._list_path).value
        with open(str(f(_list_path)/'mutants.list.csv'), 'a') as hid:
            hid.write('%s;%s\n' % (';'.join(self._mutant.entry), _output_path))

class GenerateCoveragedataForMutants(ProcessMutantsPhase):
    def generateSteps(self, _by, _from, _output_path, _to):
        self._steps = []
        for mutant in self.mutants[_from:_to:_by]:
            print(info("Creating step for mutant '%s'" % as_proper(mutant.key)))
            if not hasattr(mutant, 'real_index'):
                pdb.set_trace()
            step = GenerateCoverageDataForMutant(mutant, f(_output_path) / 'data' / str(mutant.real_index), _output_path)
            self._steps.append(step)

class ConvertCloverCoverageDataToSodaMatrix(Call):
    def __init__(self, clover_data_path):
        self._clover_data_path = clover_data_path

    def _do(self, *args, **kvargs):
        _clover_data_path = CleverString(self._clover_data_path)._value
        Need(aString('soda_jni_path')).do()
        Need(aString('soda_clover2soda_path')).do()
        mergeData = str(f(_clover_data_path)/'raw'/'cloverMerge.db')
        singleData = str(f(_clover_data_path)/'raw'/'clover.db')
        try:
            data_path = eitherFile(mergeData, singleData)
        except FileNotFoundError as e:
            print(error("Neither %s nor %s have found." % (as_proper(mergeData), as_proper(singleData))))
            raise e
        self._command = 'java -Djava.library.path=${soda_jni_path} -jar ${soda_clover2soda_path} -d %s -c %s' % (data_path, f(_clover_data_path)/'..'/'coverage.sodabin')
        super()._do(*args, **kvargs)

print(info("%s is loaded." % as_proper("Mutant handling")))