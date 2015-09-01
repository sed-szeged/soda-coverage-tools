from .maven_cover_res import *
from .structure import *
from .need import *
from .call import *
from .filetweak import *
import os
import xml.etree.ElementTree as ET

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
            if os.path.dirname(path) == self._src:
                return path

    def _detectTestingFrameWork(self):
        for path in self._poms:
            tree = ET.parse(path)
            root = tree.getroot()
            res = root.findall(".//mvn:dependency[mvn:artifactId='testng']", ns)
            if res:
                self._profile = soda_coverage_profile
                print(info(as_proper("Detected TestNG testing framework.")))
                return
            res = root.findall(".//mvn:dependency[mvn:artifactId='junit']", ns)
            if res:
                self._profile = soda_coverage_profile_junit
                print(info(as_proper("Detected jUnit testing framework.")))
                return

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

class TransformCoverageData(Call):
    def __init__(self, src, goals='clean test'):
        #super().__init__('pwd')
        super().__init__('mvn3.3 %s hu.sed.soda.tools:soda-maven-plugin:report -Psoda-coverage' % (goals))
        self._src = src

    def _do(self, *args, **kvargs):
        super()._do(cwd=CleverString(self._src).value)
