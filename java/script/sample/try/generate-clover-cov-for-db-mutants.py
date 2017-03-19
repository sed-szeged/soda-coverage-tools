"""
This script generates coverage and results data for directory based mutants using Clover

Usage:
    python3 generate-coverage-docker.py
        output_dir=the directory where the output will be stored
        original_path=the root directory of the original project (where the pom.xml file is)
        patch_root=the root directory of the mutants (where the numbered - per mutants - directories are)
        merge_root=the directory where the mutants will be assembled (in a one directory per mutant style)
        relative_path_to_patch=the path-diff between the id (number) directory of a mutant and the original project's root directory (usually: src/main/java)
        soda_jni_path=the directory in which the libSoDAJni.so is
        soda_clover2soda_path=the Clover2SoDA tool's JAR assembly

"""

from soda import *

Phase(
    'generate coverage data',
    SetVariable(aString('external_timeout'), 60 ** 2),
    SetVariable(aString('maven'), 'mvn'),
    Need(aString('output_dir')),
    Need(aString('original_path')),
    Need(aString('patch_root')),
    Need(aString('merge_root')),
    Need(aString('relative_path_to_patch')),
    Need(aString('soda_jni_path')),
    Need(aString('soda_clover2soda_path')),
    GenerateCoveragedataForMutants(
        'execute tests',
        '${output_dir}',
        MutantsPatchLoader(
            '${original_path}',
            '${patch_root}',
            '${merge_root}',
            '${relative_path_to_patch}'
        )
    )
).do()
