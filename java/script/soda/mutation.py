from .structure import *
from .feedback import *
from .need import *
from .filetweak import *
import glob
import re
import abc
import json #https://docs.python.org/3.4/library/json.html

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
        return json.dumps({'keyword':self.keyword, 'param':self.param, 'data':self.data})

class MutationType:
    none = 'none'
    returnType = 'return'
    ifType = 'if'
    variableSwitchType = 'variable_switch'
    statementDeletionType = 'statement_deletion'

class SodaAnnotationAction(metaclass=abc.ABCMeta):
    def __init__(self, executor):
        self._executor = executor
        self.stack = []
        self._state = {}

    @abc.abstractmethod
    def Apply(self, line, state, **kvargs):
        pass

class DumpAction(SodaAnnotationAction):
    def Apply(self, line, state, **kvargs):
        if not self.stack:
            return None
        last = self.stack[-1]
        print(info('the last annotation was %s' % as_sample(last)))

class DisableMutationAction(SodaAnnotationAction):
    def Apply(self, line, state, **kvargs):
        if not self.stack:
            return None
        last = self.stack[-1]
        if last.keyword == 'begin' and last.param == 'mutation' and last.data['type'] == self._executor._mutation_type:
            state['in_mutation'] = True
            self.stack.pop()
            print(info("Step into mutation declaration."))
        elif last.keyword == 'end' and last.param == 'mutation':
            state['in_mutation'] = False
            print(info("Leave mutation declaration."))
            self.stack.pop()
        elif not isAnnotation(line) and state.get('in_mutation', False):
            print(info("Emmit disabled source code line."))
            return '//%s //disabled by SoDA Python API' % line

class InsertInstrumentationCodeAction(SodaAnnotationAction):
    def __init__(self, executor):
        super().__init__(executor)
        self._mutation_count = 0

    def Apply(self, line, state, **kvargs):
        if not self.stack:
            return None
        last = self.stack[-1]
        if (last.keyword == 'begin' and last.param == 'mutation' and last.data['type'] == self._executor._mutation_type) or (last.keyword == 'begin' and last.param == 'method'):
            print(info("Insert instrumentation source code line."))
            self.stack.pop()
            data = {'mutation': {'type': self._executor._mutation_type}, 'file': {}}
            if last.param == 'mutation':
                data['mutation']['count'] = self._mutation_count
                self._mutation_count += 1
            if 'source_path' in kvargs:
                data['file']['relative-path'] = kvargs['source_path'][1:]
            return '%s\nhu.sed.soda.tools.SimpleInstrumentationListener.recordCoverage("%s");' % (line, json.dumps(data).replace('"', '\\"'))

class CreateInstrumentedCodeBase(Doable):
    def __init__(self, annotated_path, result_path, mutation_type):
        self._annotated_path = annotated_path
        self._result_path = result_path
        self._mutation_type = mutation_type

        self._state = {}

    def _init_actions(self):
        #self._actions = [cls(self) for cls in SodaAnnotationAction.__subclasses__()]
        self._actions = [DisableMutationAction(self), InsertInstrumentationCodeAction(self)]

    def _do(self, *args, **kvargs):
        _annotated_path = CleverString(self._annotated_path).value
        _result_path = CleverString(self._result_path).value
        _mutation_type = CleverString(self._mutation_type).value
        DeleteFolder(_result_path).do()
        instrumented_path = f(_result_path)/'instrumented'
        Copy(_annotated_path, instrumented_path).do()
        sourceFiles = glob.glob(str(f(instrumented_path)/'*.java'))
        for source in sourceFiles:
            original = '%s.original' % source
            Copy(source, original).do()
            with open(source, 'w') as source_file, open(original, 'r') as original_file:
                self._init_actions()
                self._state = {}
                for index, line in enumerate(original_file):
                    if isAnnotation(line):
                        print(info("Annotation found at %s:%s") % (as_proper(source.replace('_result_path','')), as_proper(index)))
                        for action in self._actions:
                            action.stack.append(SodaAnnotation(line))
                    new_lines = []
                    for action in self._actions:
                        new_line = action.Apply(line.rstrip(), self._state, source_path=source.replace(str(instrumented_path),''))
                        if new_line:
                            new_lines.append(new_line)
                    if new_lines:
                        for new_line in new_lines:
                            source_file.write('%s\n' % new_line)
                    else:
                        source_file.write(line)

print(info("%s is loaded" % as_proper("Program Mutation support")))