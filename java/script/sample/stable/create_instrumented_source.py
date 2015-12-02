#python3.4 create_instrumented_source.py annotated_source=/home/geryxyz/mapdb instrumented_source=/home/geryxyz/instrumented_result coverage=/home/geryxyz/coverage soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader

from soda import *

Phase('generate instrumented code',
    SetVariable(aString('external_timeout'), 3600),
    Need(aString('annotated_source')),
    Need(aString('instrumented_source')),
    DeleteFolder('${instrumented_source}'),
    CreateInstrumentedCodeBase('${annotated_source}', '${instrumented_source}')
).do()

Phase('generate matrices',
    Need(aString('coverage')),
    TransformCoverageData('${instrumented_source}', CoverageEngine.Manual),
    CollectFiles('${instrumented_source}', 'target/jacoco/TestCoverage.csv', f('${coverage}')/'raw'),
    CreateCovarageMatrix(f('${coverage}')/'raw'/'TestCoverage.csv', None, f('${coverage}')/'coverage-matrix', f('${instrumented_source}')/'instrumentation.log.txt', engine=CoverageEngine.Manual)
).do()