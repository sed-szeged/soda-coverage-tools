from soda import * 
import os

pj = os.path.join

Phase('load arguments',
    Need(aString('git_url')),
    Need(aString('repository_path')),
    Need(aString('source_path')),
    Need(aString('pom_path')),
    Need(aString('output_path'))
).do()

for commit in From(GitRepo('${git_url}')).to('${repository_path}').checkout().all():
    commitStr = str(commit)
    Phase('run tests',
        AddSodaProfileWithJUnitTo('${pom_path}'),
        TransformCoverageData('${source_path}'),
        Restore('${pom_path}'),
        CollectFiles('${source_path}', '${source_path}/**/jacoco', pj('${output_path}', commitStr)),
        CreateCovarageMatrix(pj('${output_path}', commitStr, 'coverage', 'xml'), MatrixGranuality.method, pj('${output_path}', commitStr, 'coverage-matrix'))
    ).do()