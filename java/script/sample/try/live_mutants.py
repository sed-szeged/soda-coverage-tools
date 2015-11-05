#python3.4 git_url= mutant_source=_mutants mutation_type=return live_mutants.py mutants_path=/home/geryxyz/mutants output_path=/home/geryxyz/mutants_binaries

from soda import *

Phase('collect parameters',
      Need(aString('mutants_path')),
      Need(aString('output_path')),
      Need(aString('git_url'))
).do()

Phase('generate mutants',
    From(GitRepo('${git_url}')).to('${source_path}').checkout('HEAD'),
    Need(aString('mutant_source')),
    Need(aString('mutation_type')),
    CreateMutants('${source_path}', '${mutant_source}', '${mutation_type}')
)

for index, mutant in enumerate(FromDirectory('${mutants_path}').getMutants()):
    mutant.generateTestResults(f('${output_path}')/str(index+1)).do()