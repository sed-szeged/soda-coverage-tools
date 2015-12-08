#python3.4 calculate_testscore.py mutant_testresult=/home/geryxyz/soda-results/mutation/mapdb/if/mutants_testresults soda_rawDataReader_path=/home/geryxyz/soda_build/cl/SoDATools/utilities/rawdatareader soda_mutationScore_path=/home/geryxyz/soda_build/cl/SoDATools/mutation-score/mutation-score

from soda import *

Phase('init',
    SetVariable(aString('external_timeout'), 60 ** 2)
).do()

Phase('generate test results',
    Need(aString('mutant_testresult')),
    CreateResultsMatrix(f('${mutant_testresult}')/'data', 'dejagnu-one-revision-per-file', f('${mutant_testresult}')/'results-matrix'),
    GenerateTestScore(f('${mutant_testresult}')/'results-matrix', f('${mutant_testresult}')/'metric'/'testscore.csv')
).do()
