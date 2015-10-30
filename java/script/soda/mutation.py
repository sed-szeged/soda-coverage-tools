import json #https://docs.python.org/3.4/library/json.html
from .filetweak import *
from .stringutil import *
import glob2
from deepdiff import DeepDiff as hasDiff #https://github.com/seperman/deepdiff
import hashlib
import os


def isAnnotation(line):
    return line.startswith('//SZTE_SODA')

class SodaAnnotation:
    def __init__(self, line):
        line = line.strip()
        if not isAnnotation(line):
            raise AttributeError('Line "%s" is not a SoDA annotation.' % line)
        match = re.search(r'//SZTE_SODA\s(?P<keyword>\w+)\s(?P<param>\w+)\s?(?P<data>[\w\W]*)$', line)
        if match:
            print(info("Processed line was '%s'" % as_sample(line)))
            self.keyword = match.group('keyword').lower()
            self.param = match.group('param').lower()
            data = match.group('data')
            if data:
                self.data = json.loads(data)
            else:
                self.data = []
        else:
            raise AttributeError('Unsupported annotation format in "%s".' % as_sample(line))

    def __str__(self):
        return json.dumps(self.toJSON())

    def toJSON(self):
        return {'keyword': self.keyword, 'param': self.param, 'data': self.data}


class MutationType:
    none = 'none'
    returnType = 'return'
    ifType = 'if'
    variableSwitchType = 'variable_switch'
    statementDeletionType = 'statement_deletion'

class SodaAnnotationAction(metaclass=abc.ABCMeta):
    def __init__(self, executor):
        self._mutation_count = 0
        self._executor = executor
        self.stack = []
        self._state = {}

    def reset(self):
        self._mutation_count = 0

    @abc.abstractmethod
    def Apply(self, line, state, **kvargs):
        pass

    def createID(self, annotation, **kvargs):
        data = {'annotation': annotation.toJSON()}
        if annotation.param == 'mutation':
            data['mutation'] = {}
            data['mutation']['type'] = self._executor._mutation_type
            data['mutation']['count'] = self._mutation_count
            self._mutation_count += 1
        if 'source_path' in kvargs:
            data['file'] = {}
            data['file']['relative_path'] = kvargs['source_path'][1:]
        return data


class DumpAction(SodaAnnotationAction):
    def Apply(self, line, state, **kvargs):
        if not self.stack:
            return None
        last = self.stack[-1]
        print(info('the last annotation was %s' % as_sample(last)))

class MutationFlavor:
    original = 'original'
    modified = 'modified'

class DetectMutationAction(SodaAnnotationAction):
    def __init__(self, executor):
        super().__init__(executor)

    def Apply(self, line, state, **kvargs):
        if 'mutation_start' in state:
            del state['mutation_start']
        if 'mutation_end' in state:
            del state['mutation_end']
        if self.stack:
            last = self.stack[-1]
            if last.keyword == 'begin' and last.param == 'mutation':
                state['mutation_start'] = True
                state['in_mutation'] = True
                state['mutation_id'] = self.createID(last, **kvargs)
                state['mutation_flavor'] = MutationFlavor.original
                state['mutation_type'] = last.data['type']
                self.stack.pop()
                print(info("Step into mutation declaration."))
                print(info("Step into original flavor."))
            elif last.keyword == 'end':
                if last.param == 'mutation':
                    state['mutation_end'] = True
                    state['in_mutation'] = False
                    del state['mutation_flavor']
#                    del state['mutation_type']
#                    del state['mutation_id']
                    print(info("Leave mutation declaration."))
                    self.stack.pop()
                elif last.param == 'original':
                    state['mutation_flavor'] = MutationFlavor.modified
                    print(info("Leave original flavor."))
                    print(info("Step into modified flavor."))
                    self.stack.pop()

class DisableMutationAction(SodaAnnotationAction):
    def Apply(self, line, state, **kvargs):
        if state.get('mutation_flavor', None) == MutationFlavor.original:
            print(info("Emmit original source code line."))
            return line
        elif state.get('mutation_flavor', None) == MutationFlavor.modified:
            print(info("Suppress modified source code line."))
            return '//%s //pySoDA: disabled' % line

class InsertInstrumentationCodeAction(SodaAnnotationAction):
    def __init__(self, executor):
        super().__init__(executor)

    def Apply(self, line, state, **kvargs):
        if self.stack:
            last = self.stack[-1]
            if (last.keyword == 'begin' and last.param == 'mutation') or (last.keyword == 'begin' and last.param == 'method'):
                print(info("Insert instrumentation source code line."))
                self.stack.pop()
                data = self.createID(last, **kvargs)
                return 'hu.sed.soda.tools.SimpleInstrumentationListener.recordCoverage("%s"); //pySoDA: instrumentation code' % json.dumps(data).replace('"', '\\"')


class ModifySourceCode(Doable, metaclass=abc.ABCMeta):
    def __init__(self, original_path, result_path, ):
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
        super().__init__(original_path, result_path)
        self._mutation_type = mutation_type

class EnableMutationAction(SodaAnnotationAction):
    def __init__(self, executor):
        super().__init__(executor)
        self._last_enabled_mutation = None
        self._enable_next_mutation = True

    def Apply(self, line, state, **kvargs):

        if state.get('mutation_start', False):
            if not hasDiff(state.get('mutation_id', None), self._last_enabled_mutation):
                self._enable_next_mutation = True
                print(info("Enable next mutation."))
        if state.get('mutation_end', False):
            if self._enable_next_mutation and hasDiff(state.get('mutation_id', None), self._last_enabled_mutation):
                self._enable_next_mutation = False
                print(info("Disable next mutation."))
                self._last_enabled_mutation = state['mutation_id']
                self._executor.enabled_mutation_id = self._last_enabled_mutation
                print(info("Mark mutation '%s' as last enabled." % as_proper(state['mutation_id'])))

        if self._enable_next_mutation and hasDiff(state.get('mutation_id', None), self._last_enabled_mutation):
            if state.get('mutation_flavor', None) == MutationFlavor.original:
                print(info("Suppress original source code line."))
                return '//%s //pySoDA: disabled' % line
            elif state.get('mutation_flavor', None) == MutationFlavor.modified:
                print(info("Emit modified source code line."))
                return line
        else:
            if state.get('mutation_flavor', None) == MutationFlavor.original:
                print(info("Emmit original source code line."))
                return line
            elif state.get('mutation_flavor', None) == MutationFlavor.modified:
                print(info("Suppress modified source code line."))
                return '//%s //pySoDA: disabled' % line


class CountMutationsAction(SodaAnnotationAction):
    def Apply(self, line, state, **kvargs):
        if self.stack:
            last = self.stack[-1]
            if last.keyword == 'begin' and last.param == 'mutation' and last.data['type'] == self._executor._mutation_type:
                state['mutation_index'] = state.get('mutation_index', -1) + 1

class ModifySourceCodeWithPersistentActionSate(ModifySourceCode):
    def __init__(self, original_path, result_path, *actions):
        super().__init__(original_path, result_path)
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
            DetectMutationAction, EnableMutationAction
        )
        mutantCreator._mutation_type = _mutation_type

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