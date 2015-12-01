#python3.4 create_instrumented_source.py annotated_source=/home/geryxyz/mutation_test instrumented_source=/home/geryxyz/instrumented_result mutation_type=return

from soda import *

Phase('generate instrumented code',
    Need(aString('annotated_source')),
    Need(aString('instrumented_source')),
    DeleteFolder('${instrumented_source}'),
    CreateInstrumentedCodeBase('${annotated_source}', '${instrumented_source}', '${mutation_type}')
).do()