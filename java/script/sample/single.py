#usage (example):
#python3.4 single.py git_url=https://github.com/junit-team/junit.git repository_path=/home/user/testRepo source_path=/home/user/testRepo pom_path=/home/user/testRepo/pom.xml output_path=/home/user/testRepo_result soda_rawDataReader_path=/home/user/soda-build/cl/SoDATools/utilities/rawdatareader

from soda import * 
import os

pj = os.path.join

Phase('load arguments',
    Need(aString('git_url')),
    Need(aString('repository_path')),
    Need(aString('source_path')),
    Need(aString('pom_path')),
    Need(aString('output_path'))
).do()

revision_number = 0
for commit in From(GitRepo('${git_url}')).to('${repository_path}').checkout('master').between("2015-07-01", "2015-07-05"):
    revision_number += 1
    commitStr = str(commit)
    Phase('run tests',
        AddSodaProfileWithJUnitTo('${pom_path}'),
        TransformCoverageData('${source_path}'),
        Restore('${pom_path}'),
        CollectFiles('${source_path}', 'target/jacoco/coverage/xml', pj('${output_path}', commitStr, 'raw-coverage-data','xml')),
        CreateCovarageMatrix(pj('${output_path}', commitStr, 'raw-coverage-data', 'xml'), MatrixGranuality.method, pj('${output_path}', commitStr, 'coverage-matrix')),
        CollectFiles('${source_path}', 'target/jacoco/0/TestResults.r0', pj('${output_path}', commitStr, 'raw-test-data', str(revision_number))),
        CreateResultsMatrix(pj('${output_path}', commitStr, 'raw-test-data'), 'dejagnu-one-revision-per-file', pj('${output_path}', commitStr, 'results-matrix'))
    ).do()