import json

from .filetweak import *
from .feedback import info, as_sample


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
            data['mutation']['type'] = annotation.data['type']
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


