from .structure import *
from .feedback import *
from .call import *
from .soda_res import *
import copy
import json
from .filetweak import *

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
    def __init__(self, config_path):
        Need(aString('soda_testSuiteMetrics_path')).do()
        super().__init__("%s %s" % ('${soda_testSuiteMetrics_path}', config_path))