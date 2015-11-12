#python3.4 generate_mutants_testresults.py git_url=/home/geryxyz/repos/oryx.git original_source=/home/geryxyz/original_source annotated_source=/home/geryxyz/annotated_source mutant_source=/home/geryxyz/mutant_source mutation_type=return mutant_testresult=/home/geryxyz/mutants_testresults

from soda import *

Phase('generate mutants',
    Need(aString('git_url')),
    Need(aString('annotated_source')),
    From(GitRepo('${git_url}')).to('${annotated_source}').checkout('sed-mutations'),
    Need(aString('mutant_source')),
    Need(aString('mutation_type')),
    CreateMutants('${annotated_source}', '${mutant_source}', '${mutation_type}')
).do()

Phase('generate test results',
    DeleteFolder('${mutant_testresult}'),
    Phase('generate test results for original',
        Need(aString('original_source')),
        From(GitRepo('${git_url}')).to('${original_source}').checkout('sed-poms'),
        CallMaven(['clean', 'test'], ['soda-dump-test-results']).From('${original_source}'),
        CollectFiles('${original_source}', f('target')/'jacoco'/'0'/'TestResults.r0', f('${mutant_testresult}')/'data'/str(0))
    ),
    Need(aString('mutant_testresult')),
    ParalellGenerateTestResultForMutants('test mutants', '${mutant_testresult}', FromDirectory('${mutant_source}').getMutants(), name_of_workers=developers_of_soda).fromMutant(0).to(3)
#    GenerateTestResultForMutants('test mutants', '${mutant_testresult}', FromDirectory('${mutant_source}').getMutants()).fromMutant(0).to(3)
).do()
