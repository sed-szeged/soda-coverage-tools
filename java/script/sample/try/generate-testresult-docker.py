#python3.4 generate-testresult-docker.py output_dir=/home/geryxyz/major/testresults/ original_path=/home/geryxyz/major/joda-time patch_root=/home/geryxyz/major/joda-time-mutants merge_root=/home/geryxyz/major/joda-time-merge2 relative_path_to_patch=src/main/java
from soda import *

Phase(
    'generate test results',
    SetVariable(aString('external_timeout'), 60 ** 2),
    SetVariable(aString('maven'), 'mvn'),
    Need(aString('output_dir')),
    Need(aString('original_path')),
    Need(aString('patch_root')),
    Need(aString('merge_root')),
    Need(aString('relative_path_to_patch')),
    ParalellGenerateTestResultForMutants(
        'execute tests',
        '${output_dir}',
        MutantsPatchLoader(
            '${original_path}',
            '${patch_root}',
            '${merge_root}',
            '${relative_path_to_patch}'),
        valar)
).do()