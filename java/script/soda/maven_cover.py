from .maven_cover_res import *
from .structure import *
from .need import *
from .call import *
from .filetweak import *
import os

print(info(as_proper("Soda Maven Coverage")+" support is loaded."))

class AddSodaProfileTo(Doable):
    def __init__(self, pom):
        self._pom = pom

    def _do(self):
        insert(soda_coverage_profile, CleverString(self._pom).value, '</profiles>')

class AddSodaProfileWithJUnitTo(Doable):
    def __init__(self, pom):
        self._pom = pom

    def _do(self):
        insert(soda_coverage_profile_junit, CleverString(self._pom).value, '</profiles>')

class TransformCoverageData(Call):
    def __init__(self, src, goals='clean test'):
        #super().__init__('pwd')
        super().__init__('mvn3.3 %s hu.sed.soda.tools:soda-maven-plugin:report -Psoda-coverage' % (goals))
        self._src = src

    def _do(self, *args, **kvargs):
        super()._do(cwd=CleverString(self._src).value)
