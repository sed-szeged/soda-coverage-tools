import subprocess as sp #https://docs.python.org/3.4/library/subprocess.html
from .need import *
from .feedback import *
from .structure import *
import datetime

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
        Need(aString('external_timeout')).do()
        timeout = int(CleverString('${external_timeout}').value)
        if settings.mode > FeedbackModes.quite:
            try:
                sp.call(command, shell=True, timeout=timeout, *args, **kvargs)
            except sp.TimeoutExpired:
                print(error('External call was killed after %s seconds' % as_sample(timeout)))
        else:
            print(warn("Quite mode enabled, all output of the external calls will redirect into log files."))
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
            thread_name = threading.current_thread().name
            logfile_name = 'ON_%s_Call_%s.log' % (thread_name, timestamp)
            with open(logfile_name, 'w') as log:
                log.write('the exact command was the following:\n\n%s\n\n' % command)
            try:
                with open(logfile_name, 'a') as log:
                    sp.call(command, shell=True, stdout=log, stderr=log, timeout=timeout, *args, **kvargs)
            except sp.TimeoutExpired:
                print(error('External call was killed after %s seconds' % as_sample(timeout)))
                with open(logfile_name, 'a') as log:
                    log.write('\n\nExternal call was killed after %s seconds' % timeout)

class CallRawDataReader(Call):
    def __init__(self, readerType, mode, granularity, path, output):
        super().__init__('${soda_rawDataReader_path}/rawDataReader -t %s -m %s -g %s -p %s -o %s' % (readerType, mode, granularity, path, output))

    def _do(self, *args, **kvargs):
       Need(aString('soda_rawDataReader_path'))._do(*args, **kvargs)
       super()._do(*args, **kvargs)

class CallMaven(Call):
    def __init__(self, phases, profiles, *args, **kvargs):
        super().__init__('mvn3.3 %s -P%s' % (' '.join(phases), ','.join(profiles)))
        self._args = args
        self._kvargs = kvargs
        self._path = None

    def From(self, path):
        self._path = path
        return self

    def _do(self, *args, **kvargs):
        self._args += args
        self._kvargs.update(kvargs)
        if self._path:
            self._kvargs.update({'cwd': CleverString(self._path).value})
        super()._do(*self._args, **self._kvargs)
