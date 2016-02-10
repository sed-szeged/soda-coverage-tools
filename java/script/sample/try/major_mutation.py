#python3.4 major_mutation.py original_path=/home/geryxyz/major/joda-time patch_root=/home/geryxyz/major/joda-time-mutants merge_root=/home/geryxyz/major/joda-time-merge relative_path_to_patch=src/main/java log_path=/home/geryxyz/major/mutants.log

from soda import *

Phase('init',
	Need(aString('original_path')),
	Need(aString('patch_root')),
	Need(aString('merge_root')),
	Need(aString('relative_path_to_patch')),
	Need(aString('log_path'))
).do()

Phase('create mutated codebases',
	MergeAllSubdirectories('applying patches','${original_path}', '${patch_root}', '${merge_root}', relative_path_to_patch='${relative_path_to_patch}'),
	DictionariesToMutantList('${merge_root}', f('${merge_root}')/'list.csv', MajorIdenticalChangeFilter('${log_path}'))
).do()