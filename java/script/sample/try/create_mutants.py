#python3.4 create_mutants.py annotated_source=/home/geryxyz/mutation_test mutant_source=/home/geryxyz/instrumented_result

from soda import *

Phase('generate instrumented code',
    Need(aString('annotated_source')),
    Need(aString('mutant_source')),
    CreateMutants('${annotated_source}', '${mutant_source}', MutationType.returnType)
).do()