#python3.4 calculate_testscore.py project=oryx mutant_testresult=/home/geryxyz/mutants_testresults soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_testSuiteMetrics_path=/home/geryxyz/soda_build/cl/SoDATools/test-suite-metrics/test-suite-metrics

from soda import *

Phase('init',
    SetVariable(aString('external_timeout'), 60 ** 2)
).do()

Phase('generate test results',
    Need(aString('mutant_testresult')),
    CreateResultsMatrix(f('${mutant_testresult}')/'data', 'dejagnu-one-revision-per-file', f('${mutant_testresult}')/'results-matrix'),
    Need(aString('project')),
    GenerateJSONConfig(f('${mutant_testresult}')/'config.JSON', f('${mutant_testresult}')/'results-matrix', '${project}', f('${mutant_testresult}')/'metric'),
    GenerateTestScore(f('${mutant_testresult}')/'config.JSON')
).do()
