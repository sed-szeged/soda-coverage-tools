#usage (example):
#python3.4 multi_from_git.py git_url=https://github.com/junit-team/junit.git repository_path=/home/geryxyz/testRepo from=2015-07-01 to=2015-07-05 source_path=/home/geryxyz/testRepo pom_path=/home/geryxyz/testRepo/pom.xml output_path=/home/geryxyz/testRepo_result soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader

from soda import * 
import os

Phase('load arguments',
    Need(aString('git_url')),
    Need(aString('repository_path')),
    Need(aString('from')),
    Need(aString('to')),
    Need(aString('source_path')),
    Need(aString('pom_path')),
    Need(aString('output_path'))
).do()

revision_number = 0
for commit in From(GitRepo('${git_url}')).to('${repository_path}').checkout('master').between('${from}', '${to}'):
    revision_number += 1
    Phase('run tests',
        AddSodaProfileWithJUnitTo('${pom_path}'),
        TransformCoverageData('${source_path}'),
        Restore('${pom_path}'),
        CollectFiles(
            '${source_path}',
            'target/jacoco/coverage/xml',
            pj('${output_path}', commit, 'raw-coverage-data','xml')),
        CreateCovarageMatrix(pj('${output_path}', commit, 'raw-coverage-data', 'xml'), MatrixGranuality.method, pj('${output_path}', commit, 'coverage-matrix')),
        CollectFiles('${source_path}', 'target/jacoco/0/TestResults.r0', pj('${output_path}', commit, 'raw-test-data', revision_number)),
        CreateResultsMatrix(pj('${output_path}', commit, 'raw-test-data'), 'dejagnu-one-revision-per-file', pj('${output_path}', commit, 'results-matrix'))
    ).do()