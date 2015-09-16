#python3.4 03-repo.py git_url=https://github.com/junit-team/junit.git source_path=demoRepo from=2015-07-01 to=2015-07-05

from soda import *

Phase("parameters",
    Need(aString('git_url')),
    Need(aString('source_path'))
).do()

for commit in From(GitRepo('${git_url}')).to('${source_path}').checkout('master').between('${from}', '${to}'):
    Phase("measuring revision",
        Need(aString(commit))
    ).do()