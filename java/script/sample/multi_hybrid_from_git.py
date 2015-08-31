#usage (example):
#python3.4 multi_hybrid_from_git.py git_url=https://github.com/junit-team/junit.git repository_path=/home/geryxyz/multi_hybrid_repo source_path=. pom_path=pom.xml output_path=/home/geryxyz/multi_hybrid_test_results soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader from=2015-07-01 to=2015-07-05

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
for mom, dad in pairwise(From(GitRepo('${git_url}')).to('${repository_path}').checkout('master').all()):
    if not mom or not dad:
        break
    hybrid_id = '%s_%d_%s' % (mom, revision_number, dad)
    Phase('analyze hybrid',
        Phase('checkout',
            Need(aString('git_url')),
            Need(aString('repository_path')),
            SetVariable(aString('mom_hash'), mom),
            SetVariable(aString('dad_hash'), dad),
            SetVariable(aString('mom_path'), f('${repository_path}')/'mom'),
            SetVariable(aString('dad_path'), f('${repository_path}')/'dad'),
            SetVariable(aString('child_path'), f('${repository_path}')/'child'),
            From(GitRepo('${git_url}')).to('${mom_path}').checkout('${mom_hash}'),
            From(GitRepo('${git_url}')).to('${dad_path}').checkout('${dad_hash}'),
            From(GitRepo('${git_url}')).to('${child_path}').checkout('${mom_hash}')
        ),
        Phase('run tests',
            CopyMatching('${dad_path}', '${child_path}', f('**')/'src'/'test'),
            Need(aString('source_path')),
            Need(aString('pom_path')),
            AddSodaProfileTo(f('${child_path}')/'${pom_path}'),
            TransformCoverageData(f('${child_path}')/'${source_path}'),
            Restore(f('${child_path}')/'${pom_path}')
        ),
        Phase('create results',
            Need(aString('output_path')),
            DeleteFolder(f('${output_path}')/'raw-coverage-data'/'xml'),
            CollectFiles(f('${child_path}')/'${source_path}', 'target/jacoco/coverage/xml', f('${output_path}')/'raw-coverage-data'/'xml'),
            CreateCovarageMatrix(f('${output_path}')/'raw-coverage-data'/'xml', MatrixGranuality.method, f('${output_path}')/hybrid_id/'coverage-matrix'),
            LogFile(f('${output_path}')/hybrid_id/'coverage-matrix', size_of, f('${output_path}')/'size_hybrid.log.csv'),
            CollectFiles(f('${child_path}')/'${source_path}', 'target/jacoco/0/TestResults.r0', f('${output_path}')/hybrid_id/'raw-test-data'),
            CreateResultsMatrix(f('${output_path}')/hybrid_id/'raw-test-data', 'dejagnu-one-revision-per-file', f('${output_path}')/hybrid_id/'results-matrix')
        )
    ).do()
    revision_number += 1