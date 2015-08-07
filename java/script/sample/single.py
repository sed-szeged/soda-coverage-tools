from soda import * 
import os

pj = os.path.join

Phase('checkout',
    Need(aString('git_url')),
    Need(aString('repository_path')),
    From(GitRepo('${git_url}')).to('${repository_path}')
).do()

MergeResults = Phase('merge results',
    MergeMatchingFiles('${output_path}/HashToTest', '${source_path}/**/target/jacoco/**/HashToTest.*'),
    MergeMatchingFiles('${output_path}/TestResults', '${source_path}/**/target/jacoco/**/TestResults.*')
)

Phase('run tests',
    Need(aString('source_path')),
    Need(aString('pom_path')),
    Need(aString('output_path')),
    AddSodaProfileWithJUnitTo('${pom_path}'),
    TransformCoverageData('${source_path}'),
    Restore('${pom_path}'),
    CollectFiles(pj('${source_path}'), 'target/jacoco/coverage/xml', pj('${output_path}', 'coverage-xml-data')),
    MergeResults,
    CreateCovarageMatrix(pj('${output_path}', 'coverage-xml-data'), MatrixGranuality.method, pj('${output_path}', 'CoverageMatrix'))
).do()