from .maven_cover_res import *
from .structure import *
from .filetweak import *
from .need import *
from .call import *
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
    def __init__(self, src):
        #super().__init__('pwd')
        super().__init__('mvn3.3 clean test hu.sed.soda.tools:soda-maven-plugin:report -Psoda-coverage')
        self._src = src

    def _do(self, *args, **kvargs):
        super()._do(cwd=CleverString(self._src).value)
