from soda import * 

Phase('run tests',
    Need(aString('source_path')),
    Need(aString('pom_path')),
    AddSodaProfileWithJUnitTo('${pom_path}'),
    TransformCoverageData('${source_path}'),
    Restore('${pom_path}')
).do()
