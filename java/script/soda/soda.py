from .structure import *
from .feedback import *
from .call import *

class MatrixGranuality(object):
    package = "package"
    source = "src"
    class_ = "class"
    method = "method"

class CreateCovarageMatrix(CallRawDataReader):
    def __init__(self, path, granularity, output):
        super().__init__('coverage', 'jacoco-java', granularity, path, output)

    def _do(self, *args, **kvargs):
        super()._do(*args, **kvargs)

class CreateResultsMatrix(CallRawDataReader):
    def __init__(self, path, reader, output):
        super().__init__('results', reader, MatrixGranuality.method, path, output)

    def _do(self, *args, **kvargs):
        super()._do(*args, **kvargs)

