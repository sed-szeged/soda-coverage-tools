#python3.4 generate-testresult-docker.py output_dir=/home/geryxyz/major/testresults/ list_path=/home/geryxyz/major/joda-time-merge/list.csv
from soda import *

Phase(
    'generate test results',
    SetVariable(aString('external_timeout'), 60 ** 2),
    SetVariable(aString('maven'), 'mvn'),
    Need(aString('output_dir')),
    Need(aString('list_path')),
    ParalellGenerateTestResultForMutants('execute tests', '${output_dir}', '${list_path}', developers_of_soda)
).do()