#usage (example):
#python3.4 deterministicy_check.py git_url=https://github.com/junit-team/junit.git source_path=/home/geryxyz/deterministicy_test output_path=/home/geryxyz/deterministicy_test_result soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_coverageComparator_path=/home/geryxyz/soda_build/cl/SoDATools/coverage-comparator

from soda import *

Phase('load arguments',
    Need(aString('git_url')),
    Need(aString('source_path')),
    Need(aString('output_path'))
).do()

Phase('run tests',
    IsDeterministic(f('${output_path}')/'coverage-matrix_*'),
    From(GitRepo('${git_url}')).to('${source_path}').checkout('HEAD'),
    AddSodaProfileTo('${source_path}'),
    TransformCoverageData('${source_path}'),
    Restore('${source_path}'),
    CollectFiles('${source_path}', f('target')/'jacoco'/'coverage'/'xml', f('${output_path}')/'raw-coverage-data'/'xml'),
    CreateCovarageMatrix(f('${output_path}')/'raw-coverage-data'/'xml', MatrixGranuality.method, f('${output_path}')/('coverage-matrix_%s' % timestamp())),
    CollectFiles('${source_path}', f('target')/'jacoco'/'0'/'TestResults.r0', f('${output_path}')/'raw-test-data'/'0'),
    CreateResultsMatrix(f('${output_path}')/'raw-test-data', 'dejagnu-one-revision-per-file', f('${output_path}')/('results-matrix_%s' % timestamp()))
).do()