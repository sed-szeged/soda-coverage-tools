#python3.4 create_mutants.py annotated_source=/home/geryxyz/mutation_test mutant_source=/home/geryxyz/mutants_result mutation_type=return

from soda import *

Phase('generate instrumented code',
    Need(aString('annotated_source')),
    Need(aString('mutant_source')),
    Need(aString('mutation_type')),
    CreateMutants('${annotated_source}', '${mutant_source}', '${mutation_type}')
).do()