import json
from .annotation import SodaAnnotationAction
from .feedback import info

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