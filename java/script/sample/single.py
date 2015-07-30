from soda import * 
import os

pj = os.path.join

Phase('run tests',
    Need(aString('source_path')),
    Need(aString('pom_path')),
    Need(aString('output_path')),
    AddSodaProfileWithJUnitTo('${pom_path}'),
    TransformCoverageData('${source_path}'),
    Restore('${pom_path}'),
    Copy(pj('${source_path}','target/jacoco'), pj('${output_path}', 'raw-coverage-data')),
    CreateCovarageMatrix(pj('${output_path}','raw-coverage-data','coverage','xml'), MatrixGranuality.method, pj('${output_path}', 'coverage-matrix'))
).do()
