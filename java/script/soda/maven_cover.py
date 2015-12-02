from .maven_cover_res import *
from .structure import *
from .need import *
from .call import *
from .filetweak import *
import os
import xml.etree.ElementTree as ET
import re

print(info(as_proper("Soda Maven Coverage")+" support is loaded."))

ns = { 'mvn': 'http://maven.apache.org/POM/4.0.0' }

class AddSodaProfileTo(Doable):
    def __init__(self, src):
        self._src = src
        ET.register_namespace('', 'http://maven.apache.org/POM/4.0.0')

    def _do(self):
        self._poms = collectFilePaths(CleverString(self._src).value, "pom.xml")
        self._detectTestingFrameWork()
        self._addProfile()
        self._tweakPoms()

    def _addProfile(self):
        rootpom = self._getRootPomPath()
        backup(rootpom)
        tree = ET.parse(rootpom)
        root = tree.getroot()
        nodes = root.findall("./mvn:profiles", ns)
        if not nodes:
            # we have to insert a new profiles tag
            profiles = ET.SubElement(root, 'profiles')
        else:
            profiles = nodes[0]
            # detect if we already replaced it
            sodaprofile = profiles.findall("./mvn:profile[mvn:id='soda-coverage']", ns)
            if sodaprofile:
                print(info(as_proper("No changes made with profiles.")))
                return

        print(info(as_proper("SoDA coverage profile injected.")))
        profiles.append(ET.fromstring(self._profile)) # selected during detection
        tree.write(rootpom)

    def _getRootPomPath(self):
        for path in self._poms:
            if os.path.dirname(path) == CleverString(self._src).value:
                return path

    def _detectTestingFrameWork(self):
        for path in self._poms:
            tree = ET.parse(path)
            root = tree.getroot()
            res = root.findall(".//mvn:dependency/mvn:artifactId", ns)
            #TODO: send a warning if both surefire- and simple version was used.
            isJUnit = any([re.match(r'((surefire-)?junit\d*)', r.text) for r in res])
            isTestNG = any([re.match(r'((surefire-)?testng)', r.text) for r in res])
            if isTestNG and isJUnit:
                raise ValueError("Multiply testing framework detected in " + path)
            if isTestNG:
                self._profile = soda_coverage_profile
                print(info(as_proper("Detected TestNG testing framework.")))
                return
            elif isJUnit:
                self._profile = soda_coverage_profile_junit
                print(info(as_proper("Detected jUnit testing framework.")))
                return
        raise ValueError("Unsupported, undetectable or missing testing framework in " + path)

    def _tweakPoms(self):
        # we have to fix argLine tags
        for path in self._poms:
            backup(path)
            tree = ET.parse(path)
            root = tree.getroot()
            nodes = root.findall(".//mvn:configuration/mvn:argLine", ns)
            if not nodes:
                continue
            for elem in nodes:
                if elem.text.startswith("${argLine} "):
                    continue
                elem.text = "${argLine} " + elem.text
            tree.write(path)

class CoverageEngine:
    Jacoco = 'jacoco'
    Manual = 'manual'

class TransformCoverageData(CallMaven):
    def __init__(self, src, engine=CoverageEngine.Jacoco):
        if engine == CoverageEngine.Jacoco:
            super().__init__(goals=['clean', 'test', 'hu.sed.soda.tools:soda-maven-plugin:report'], profiles=['soda-coverage'])
        elif engine == CoverageEngine.Manual:
            super().__init__(goals=['clean', 'test'], profiles=['soda-manual-coverage'], properties=['maven.test.failure.ignore=true'])
        else:
            print(error("Unknown coverage engine: '%s'" % as_proper(engine)))
        self._src = src

    def _do(self, *args, **kvargs):
        self.From(CleverString(self._src).value)
        super()._do()