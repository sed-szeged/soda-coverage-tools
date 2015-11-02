#python3.4 create_instrumented_source.py annotated_source=/home/geryxyz/mutation_test instrumented_source=/home/geryxyz/instrumented_result

from soda import *

Phase('generate instrumented code',
    Need(aString('annotated_source')),
    Need(aString('instrumented_source')),
    CreateInstrumentedCodeBase('${annotated_source}', '${instrumented_source}')
).do()