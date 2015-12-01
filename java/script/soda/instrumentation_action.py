import json
from .annotation import SodaAnnotationAction
from .feedback import info
from .need import *

class InsertInstrumentationCodeAction(SodaAnnotationAction):
    def __init__(self, executor):
        super().__init__(executor)
        self._last_method = ''

    def Apply(self, line, state, **kvargs):
        if self.stack:
            last = self.stack[-1]
            if last.keyword == 'begin' and (last.param == 'method' or last.param == 'mutation'):
                print(info("Insert instrumentation source code line."))
                self.stack.pop()
                data = self.createID(last, **kvargs)
                if last.param == 'mutation':
                    data['preceding-method'] = self._last_method
                elif last.param == 'method':
                    self._last_method = data
                self._executor.instrumentations.append(data)
                return 'hu.sed.soda.tools.SimpleInstrumentationListener.recordCoverage("%s"); //pySoDA: instrumentation code' % json.dumps(data).replace('"', '\\"')