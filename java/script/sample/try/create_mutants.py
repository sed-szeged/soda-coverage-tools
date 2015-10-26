#python3.4 create_mutants.py annotated_source=/home/geryxyz/mutation_test mutants_source=/home/geryxyz/instrumented_result

from soda import *

Phase('generate instrumented code',
    Need(aString('annotated_source')),
    Need(aString('mutants_source')),
    CreateInstrumentedCodeBase('${annotated_source}', '${mutants_source}', MutationType.returnType)
).do()