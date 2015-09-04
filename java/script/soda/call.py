import subprocess as sp #https://docs.python.org/3.4/library/subprocess.html
from .need import *
from .feedback import *
from .structure import *

print(info(as_proper("Commandline call") + " features are loaded."))

class Call(Doable):
    def __init__(self, command, splitby=' '):
        self._command = command
        self._splitby = splitby

    def setCommand(self, command):
        self._command = command

    def _do(self, *args, **kvargs):
        global settings
        command = CleverString(self._command).value
        #command = CleverString(self._command).value.split(self._splitby)
        print(info('executing: %s' % command))
        if settings.mode > FeedbackModes.quite:
            sp.call(command, shell=True, *args, **kvargs)
        else:
            print(warn("Quite mode enabled, all output of the external calls will redirect into log files."))
            with open('test.log', 'a') as log:
                sp.call(command, shell=True, stdout=log, stderr=log, *args, **kvargs)

class CallRawDataReader(Call):
    def __init__(self, readerType, mode, granularity, path, output):
        super().__init__('${soda_rawDataReader_path}/rawDataReader -t %s -m %s -g %s -p %s -o %s' % (readerType, mode, granularity, path, output))

    def _do(self, *args, **kvargs):
       Need(aString('soda_rawDataReader_path'))
       super()._do(*args, **kvargs)
