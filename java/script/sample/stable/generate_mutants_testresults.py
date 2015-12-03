#python3.4 generate_mutants_testresults.py project=oryx git_url=/home/geryxyz/repos/oryx.git original_source=/home/geryxyz/original_source annotated_source=/home/geryxyz/annotated_source mutant_source=/home/geryxyz/mutant_source mutation_type=return mutant_testresult=/home/geryxyz/mutants_testresults soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_testSuiteMetrics_path=/home/geryxyz/soda_build/cl/SoDATools/test-suite-metrics/test-suite-metrics

from soda import *

Phase('init',
    SetVariable(aString('external_timeout'), 60 ** 2)
).do()

Phase('generate mutants',
    Need(aString('git_url')),
    Need(aString('annotated_source')),
    From(GitRepo('${git_url}')).to('${annotated_source}').checkout('sed-mutations'),
    Need(aString('mutant_source')),
    Need(aString('mutation_type')),
    CreateMutants('${annotated_source}', '${mutant_source}', '${mutation_type}')
).do()

Phase('generate test results',
    Phase('generate test results for original',
        Need(aString('original_source')),
        From(GitRepo('${git_url}')).to('${original_source}').checkout('sed-poms'),
        CallMaven(['clean', 'test'], ['soda-dump-test-results']).From('${original_source}'),
        CollectFiles('${original_source}', f('target')/'jacoco'/'0'/'TestResults.r0', f('${mutant_testresult}')/'data'/str(0))
    ),
    Need(aString('mutant_testresult')),
    GenerateTestResultForMutants(
        'test mutants',
        '${mutant_testresult}',
        f('${mutant_source}')/'mutants.list.csv'#,
        #name_of_workers=developers_of_soda
    ),
    CreateResultsMatrix(f('${mutant_testresult}')/'data', 'dejagnu-one-revision-per-file', f('${mutant_testresult}')/'results-matrix'),
    Need(aString('project')),
    GenerateJSONConfig(f('${mutant_testresult}')/'config.JSON', f('${mutant_testresult}')/'results-matrix', '${project}', f('${mutant_testresult}')/'metric'),
    GenerateTestScore(f('${mutant_testresult}')/'config.JSON')
).do()
