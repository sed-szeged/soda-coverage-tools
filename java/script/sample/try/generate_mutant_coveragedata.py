#python3.4 generate_mutant_coveragedata.py mutant_source=/home/geryxyz/oryx_mTest mutant_coveragedata=/home/geryxyz/mutants_coverage

from soda import *

Phase('init',
    SetVariable(aString('external_timeout'), 60 ** 2)
).do()

Phase('generate coverage data',
    Need(aString('mutant_source')),
    Need(aString('mutant_coveragedata')),
    GenerateCoveragedataForMutants(
        'test mutants',
        '${mutant_coveragedata}',
        f('${mutant_source}')/'mutants.list.csv'
    ),
).do()
