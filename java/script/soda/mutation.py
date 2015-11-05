import hashlib

from .annotation import *
from .annotation import SodaAnnotation
from .instrumentation_action import InsertInstrumentationCodeAction
from .mutation_action import DetectMutationAction, DisableMutationAction, EnableMutationAction


class ModifySourceCode(Doable, metaclass=abc.ABCMeta):
    def __init__(self, original_path, result_path, mutation_type):
        self._mutation_type = mutation_type
        self._state = {}
        self.permanent_state = {}
        self._original_path = original_path
        self._result_path = result_path

    @abc.abstractmethod
    def _init_actions(self):
        pass

    def _do(self, *args, **kvargs):
        _original_path = CleverString(self._original_path).value
        _result_path = CleverString(self._result_path).value
        DeleteFolder(_result_path).do()
        Copy(_original_path, _result_path).do()
        sourceFiles = glob2.glob(str(f(_result_path) / '**' / '*.java'))
        for source in sourceFiles:
            original = self.createBackupFile(source)
            with open(source, 'w') as source_file, open(original, 'r') as original_file:
                self._init_actions()
                self._state = {}
                for index, line in enumerate(original_file):
                    indent()
                    if isAnnotation(line):
                        undent()
                        print(info("Annotation found at %s:%s") % (as_proper(source.replace('_result_path','')), as_proper(index)))
                        indent()
                        annotation = SodaAnnotation(line)
                        for action in self._actions:
                            action.stack.append(annotation)
                    new_lines = []
                    for action in self._actions:
                        new_line = action.Apply(line.rstrip(), self._state,
                                                source_path=source.replace(str(_result_path), ''))
                        if new_line:
                            new_lines.append(new_line)
                    self.emitNewLines(line, new_lines, source_file)
                    undent()

    def createBackupFile(self, source):
        original = '%s.original' % source
        Copy(source, original).do()
        return original

    def emitNewLines(self, line, new_lines, source_file):
        if new_lines:
            for new_line in new_lines:
                source_file.write('%s\n' % new_line)
        else:
            source_file.write(line)


class CreateInstrumentedCodeBase(ModifySourceCode):
    def _init_actions(self):
        self._actions = [DetectMutationAction(self), DisableMutationAction(self), InsertInstrumentationCodeAction(self)]

    def __init__(self, original_path, result_path, mutation_type):
        super().__init__(original_path, result_path, mutation_type)


class ModifySourceCodeWithPersistentActionSate(ModifySourceCode):
    def __init__(self, original_path, result_path, mutation_type, *actions):
        super().__init__(original_path, result_path, mutation_type)
        self._actions = [action(self) for action in actions]
        self.active_mutant = None

    def _init_actions(self):
        for action in self._actions:
            action.reset()

    def _do(self, *args, **kvargs):
        super()._do(*args, **kvargs)


class CreateMutants(Doable):
    def __init__(self, annoteted_path, mutants_path, mutation_type):
        self._mutants_path = mutants_path
        self._annoteted_path = annoteted_path
        self._mutation_type = mutation_type

    def _do(self, *args, **kvargs):
        _annoteted_path = CleverString(self._annoteted_path).value
        _mutants_path = CleverString(self._mutants_path).value
        _mutation_type = CleverString(self._mutation_type).value

        DeleteFolder(_mutants_path).do()

        temp_path = f(_mutants_path)/'_temp'
        mutantCreator = ModifySourceCodeWithPersistentActionSate(
            _annoteted_path,
            temp_path,
            _mutation_type,
            DetectMutationAction, EnableMutationAction
        )

        mutants_hids = {}
        global_mutation_index = 0
        while True:
            mutantCreator.enabled_mutation_id = None
            DeleteFolder(temp_path).do()
            mutantCreator.do()
            if mutantCreator.enabled_mutation_id:
                hashed = hashlib.md5()
                hid = '%s;%s;%s' %\
                              (mutantCreator.enabled_mutation_id['file']['relative_path'],
                               mutantCreator.enabled_mutation_id['mutation']['type'],
                               mutantCreator.enabled_mutation_id['mutation']['count'])
                hashed.update(hid.encode('utf-8'))
                mutant_path = f(_mutants_path)/('%d_%s' % (global_mutation_index, hashed.hexdigest()))
                global_mutation_index += 1
                mutants_hids[hid] = mutant_path
                os.rename(str(temp_path), str(mutant_path))
            else:
                break
        with open(str(f(_mutants_path)/'mutants.list.csv'), 'w') as hid_dump:
            for hid in mutants_hids:
                hid_dump.write('%s;%s\n' % (hid, mutants_hids[hid]))


print(info("%s is loaded" % as_proper("Program Mutation support")))

