from .structure import *
from .feedback import *
from .call import *

class MatrixGranuality(object):
    package = "package"
    source = "src"
    class_ = "class"
    method = "method"

class CreateCovarageMatrix(Call):
    def __init__(self, xmls, granuality, output_path):
        super().__init__('${soda_rawDataReader_path}/rawDataReader -t coverage -m jacoco-java -p %s -g %s -o %s' % (xmls, granuality, output_path))

    def _do(self, *args, **kvargs):
        Need(aString('soda_rawDataReader_path')).do()
        super()._do(*args, **kvargs)

class CreateResultsMatrix(Call):
    def __init__(self, dir, reader, output_path):
        super().__init__('${soda_rawDataReader_path}/rawDataReader -t results -m %s -p %s -o %s' % (reader, dir, output_path))

    def _do(self, *args, **kvargs):
        Need(aString('soda_rawDataReader_path')).do()
        super()._do(*args, **kvargs)
