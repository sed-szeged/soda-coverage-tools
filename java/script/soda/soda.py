from .structure import *
from .feedback import *
from .call import *
from .soda_res import *
import copy
import json
from .filetweak import *
from .maven_cover import *

class MatrixGranuality(object):
    package = "package"
    source = "src"
    class_ = "class"
    method = "method"

class CreateCovarageMatrix(CallRawDataReader):
    def __init__(self, path, granularity, output, listCodeElements, engine=CoverageEngine.Jacoco):
        if engine == CoverageEngine.Jacoco:
            super().__init__(readerType='coverage', mode='jacoco-java', granularity=granularity, path=path, output=output, listCodeElements=None)
        elif engine == CoverageEngine.Manual:
            super().__init__(readerType='coverage', mode='simple-instrumentation-listener-java', granularity=None, path=path, output=output, listCodeElements=listCodeElements)

    def _do(self, *args, **kvargs):
        super()._do(*args, **kvargs)

class CreateResultsMatrix(CallRawDataReader):
    def __init__(self, path, reader, output):
        super().__init__('results', reader, MatrixGranuality.method, path, output, listCodeElements=None)

    def _do(self, *args, **kvargs):
        super()._do(*args, **kvargs)

class GenerateJSONConfig(Doable):
    def __init__(self, config_path, results_data, project_name, output_dir):
        self._results_data = results_data
        self._project_name = project_name
        self._output_dir = output_dir
        self._config_path = config_path

    def _do(self, *args, **kvargs):
        _result_data = CleverString(self._results_data).value
        _project_name = CleverString(self._project_name).value
        _output_dir = CleverString(self._output_dir).value
        _config_path = CleverString(self._config_path).value
        config = copy.deepcopy(test_metrics_json_skeleton)
        config['results-data'] = _result_data
        config['output-dir'] = _output_dir
        config['project-name'] = _project_name
        with open(_config_path, 'w') as config_put:
            config_put.write(json.dumps(config))
        print(info("SoDA config file is written to '%s'." % as_proper(_config_path)))

class GenerateTestScore(Call):
    def __init__(self, matrix, output):
        Need(aString('soda_mutationScore_path')).do()
        super().__init__("%s -r %s -o %s" % ('${soda_mutationScore_path}', matrix, output))
