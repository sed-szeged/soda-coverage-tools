#python3.4 sonar_issue_compare.py base_url=http://10.6.13.7:9000 project_a=soda_clover_joda-time project_b=soda_jacoco_stock_joda-time result_dir=/home/geryxyz/sonarcubetest/results aggregate_by=rule

from soda import *

Phase('compare issues',
      Need(aString('base_url')),
      Need(aString('project_a')),
      Need(aString('project_b')),
      Need(aString('result_dir')),
      Need(aString('aggregate_by')),
      AggregateIssueCount(
          LoadIssuesFromSonarServer('${base_url}', '${project_a}'),
          '${aggregate_by}',
          f('${result_dir}')/'aggregated_${aggregate_by}_all_${project_a}.json.txt'
      ),
      AggregateIssueCount(
          LoadIssuesFromSonarServer('${base_url}', '${project_b}'),
          '${aggregate_by}',
          f('${result_dir}')/'aggregated_${aggregate_by}_all_${project_b}.json.txt'
      ),
      DiffSonarIssues(
          LoadIssuesFromSonarServer('${base_url}', '${project_a}'),
          LoadIssuesFromSonarServer('${base_url}', '${project_b}'),
          f('${result_dir}')/'only_${project_a}.json.txt',
          f('${result_dir}')/'only_${project_b}.json.txt'),
      AggregateIssueCount(
          LoadIssuesFromLog(f('${result_dir}')/'only_${project_a}.json.txt'),
          '${aggregate_by}',
          f('${result_dir}')/'aggregated_${aggregate_by}_only_${project_a}.json.txt'),
      AggregateIssueCount(
          LoadIssuesFromLog(f('${result_dir}')/'only_${project_b}.json.txt'),
          '${aggregate_by}',
          f('${result_dir}')/'aggregated_${aggregate_by}_only_${project_b}.json.txt')
).do()