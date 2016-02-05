#python3.4 generate_mutant_coveragedata.py git_url=/home/geryxyz/repos/oryx.git original_source=/home/geryxyz/original_source annotated_source=/home/geryxyz/annotated_source mutant_source=/home/geryxyz/mutant_source mutation_type=return mutant_list=/home/geryxyz/mapdb_mTest mutant_coveragedata=/home/geryxyz/mutants_coverage soda_jni_path=/home/geryxyz/soda-java/build/src/main/cpp soda_clover2soda_path=/home/geryxyz/soda-coverage-tools/java/clover2soda/target/clover2soda-0.0.1.jar

from soda import *

Phase('init',
    SetVariable(aString('external_timeout'), (60 ** 2) * 8)
).do()

Phase('generate mutants',
    Need(aString('git_url')),
    Need(aString('annotated_source')),
    From(GitRepo('${git_url}')).to('${annotated_source}').checkout('sed-mutations'),
    Need(aString('mutant_source')),
    Need(aString('mutation_type')),
    #CreateMutants('${annotated_source}', '${mutant_source}', '${mutation_type}')
).do()

Phase('generate coverage data',
    Need(aString('mutant_list')),
    Need(aString('mutant_coveragedata')),
    GenerateCoveragedataForMutants(
        'test mutants',
        '${mutant_coveragedata}',
        f('${mutant_list}')
    )
).do()