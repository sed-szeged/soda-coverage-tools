#usage (example):
#python3.4 deterministicy_check.py git_url=/home/geryxyz/repos/oryx.git source_path=/home/geryxyz/deterministicy_test output_path=/home/geryxyz/deterministicy_test_result

from soda import *

Phase('load arguments',
    Need(aString('git_url')),
    Need(aString('source_path')),
    Need(aString('output_path'))
).do()

Phase('run tests',
    Phase('generate test results for #0',
        From(GitRepo('${git_url}')).to(f('${source_path}')/'0').checkout('sed-poms'),
        CallMaven(['clean', 'test'], ['soda-dump-test-results']).From(f('${source_path}')/'0'),
        CollectFiles(f('${source_path}')/'0', f('target')/'jacoco'/'0'/'TestResults.r0', f('${output_path}')/'data0')
    ),
    Wait(30),
    Phase('generate test results for #1',
        From(GitRepo('${git_url}')).to(f('${source_path}')/'1').checkout('sed-poms'),
        CallMaven(['clean', 'test'], ['soda-dump-test-results']).From(f('${source_path}')/'1'),
        CollectFiles(f('${source_path}')/'1', f('target')/'jacoco'/'0'/'TestResults.r0', f('${output_path}')/'data1')
    ),
    ForwardCompareTestResult(f('${output_path}')/'data0'/'TestResults.r0', f('${output_path}')/'data1'/'TestResults.r0', f('${output_path}')/'deltas.csv')
).do()