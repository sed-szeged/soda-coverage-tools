#python3.4 generate_mutant_coveragedata.py mutant_source=/home/geryxyz/mapdb_mTest mutant_coveragedata=/home/geryxyz/mutants_coverage soda_jni_path=/home/geryxyz/soda-java/build/src/main/cpp soda_clover2soda_path=/home/geryxyz/soda-coverage-tools/java/clover2soda/target/clover2soda-0.0.1.jar

from soda import *

Phase('init',
    SetVariable(aString('external_timeout'), 60 ** 2)
).do()

Phase('generate coverage data',
    Need(aString('mutant_source')),
    Need(aString('mutant_coveragedata')),
    Phase('clean up',
        DeleteFolder('${mutant_coveragedata}')
    ),
    GenerateCoveragedataForMutants(
        'test mutants',
        '${mutant_coveragedata}',
        f('${mutant_source}')/'mutants.list.csv'
    ),
).do()