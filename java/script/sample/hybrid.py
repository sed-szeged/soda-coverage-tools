#usage (example):
#python3.4 hybrid.py git_url=https://github.com/junit-team/junit.git repository_path=/home/geryxyz/hybrid_repo mom_hash=3e43555e1f4df95b0a239f453af6d3226a8fef6e dad_hash=bcbf43dcaa5efee1418685a9a523dc11dedc77c7 source_path=. pom_path=pom.xml output_path=/home/geryxyz/hybrid_test_results soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader

from soda import * 
import os

Phase('checkout',
    Need(aString('git_url')),
    Need(aString('repository_path')),
    Need(aString('mom_hash')),
    Need(aString('dad_hash')),
    SetVariable(aString('mom_path'), f('${repository_path}')/'mom_${mom_hash}'),
    SetVariable(aString('dad_path'), f('${repository_path}')/'dad_${dad_hash}'),
    SetVariable(aString('child_path'), f('${repository_path}')/'child_${mom_hash}'),
    From(GitRepo('${git_url}')).to('${mom_path}').checkout('${mom_hash}'),
    From(GitRepo('${git_url}')).to('${dad_path}').checkout('${dad_hash}')
).do()

Phase('run tests',
    Copy('${mom_path}', '${child_path}'),
    CopyMatching('${dad_path}', '${child_path}', f('**')/'src'/'test'),
    Need(aString('source_path')),
    Need(aString('pom_path')),
    AddSodaProfileTo(f('${child_path}')/'${pom_path}'),
    TransformCoverageData(f('${child_path}')/'${source_path}'),
    Restore(f('${child_path}')/'${pom_path}')
).do()

Phase('create results',
    Need(aString('output_path')),
    CollectFiles(f('${child_path}')/'${source_path}', 'target/jacoco/coverage/xml', f('${output_path}')/'raw-coverage-data'/'xml'),
    CreateCovarageMatrix(f('${output_path}')/'raw-coverage-data'/'xml', MatrixGranuality.method, f('${output_path}')/'coverage-matrix'),
    CollectFiles(f('${child_path}')/'${source_path}', 'target/jacoco/0/TestResults.r0', f('${output_path}')/'raw-test-data'),
    CreateResultsMatrix(f('${output_path}')/'raw-test-data', 'dejagnu-one-revision-per-file', f('${output_path}')/'results-matrix')
).do()