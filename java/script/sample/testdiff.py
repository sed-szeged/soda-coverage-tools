#usage (example):
#python3.4 testdiff.py git_url=https://github.com/junit-team/junit.git repository_path=/home/user/testRepo hash1=3e43555e1f4df95b0a239f453af6d3226a8fef6e hash2=bcbf43dcaa5efee1418685a9a523dc11dedc77c7 source_path=. pom_path=pom.xml output_path=/home/user/testRepo_results soda_rawDataReader_path=/home/user/soda/cl/SoDATools/utilities/rawdatareader

from soda import * 
import os

pj = os.path.join

Phase('checkout',
    Need(aString('git_url')),
    Need(aString('repository_path')),
    Need(aString('hash1')),
    Need(aString('hash2')),
    From(GitRepo('${git_url}')).to(pj('${repository_path}','${hash1}')).checkout('${hash1}'),
    From(GitRepo('${git_url}')).to(pj('${repository_path}','${hash2}')).checkout('${hash2}')
).do()

Phase('run tests',
    CopyMatching(pj('${repository_path}','${hash2}'), pj('${repository_path}','${hash1}'), '**/src/test'),
    Need(aString('source_path')),
    Need(aString('pom_path')),
    AddSodaProfileTo(pj('${repository_path}','${hash1}','${pom_path}')),
    TransformCoverageData(pj('${repository_path}','${hash1}','${source_path}')),
    Restore('${pom_path}')
).do()

Phase('create results',
    Need(aString('output_path')),
    SetVariable(aString('hash1_source_path'), pj('${repository_path}','${hash1}','${source_path}')),
    CollectFiles('${hash1_source_path}', 'target/jacoco/coverage/xml', pj('${output_path}','raw-coverage-data','xml')),
    CreateCovarageMatrix(pj('${output_path}','raw-coverage-data','xml'), MatrixGranuality.method, pj('${output_path}','coverage-matrix')),
    CollectFiles('${hash1_source_path}', 'target/jacoco/0/TestResults.r0', pj('${output_path}', 'raw-test-data', '1')),
    CreateResultsMatrix(pj('${output_path}','raw-test-data'), 'dejagnu-one-revision-per-file', pj('${output_path}', 'results-matrix'))
).do()