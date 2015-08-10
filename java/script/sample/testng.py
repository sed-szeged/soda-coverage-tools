from soda import * 
import os

pj = os.path.join

Phase('run tests and generates SoDA binaries',
    Need(aString('source_path')),
    Need(aString('pom_path')),
    Need(aString('output_path')),
    AddSodaProfileTo('${pom_path}'),
    TransformCoverageData('${source_path}'),
    Restore('${pom_path}'),
    CollectFiles(pj('${source_path}'), 'target/jacoco/coverage/xml', pj('${output_path}', 'raw-coverage-data', 'xml')),
    Need(aString('coverage_name')),
    CreateCovarageMatrix(pj('${output_path}','raw-coverage-data','xml'), MatrixGranuality.method, pj('${output_path}', '${coverage_name}')),
    Need(aString('revision_number')),
    CollectFiles(pj('${source_path}'), 'target/jacoco/0/TestResults.r0', pj('${output_path}', 'raw-test-data', '${revision_number}')),
    Need(aString('results_name')),
    CreateResultsMatrix(pj('${output_path}','raw-test-data'), "dejagnu-one-revision-per-file", pj('${output_path}', '${results_name}'))
).do()
