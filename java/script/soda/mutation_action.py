from .annotation import SodaAnnotationAction
from .mutation_util import *
from .feedback import info, as_proper
from .need import *
from deepdiff import DeepDiff as hasDiff


class DetectMutationAction(SodaAnnotationAction):
    def __init__(self, executor):
        super().__init__(executor)

    def Apply(self, line, state, **kvargs):
        _mutation_type = CleverString(self._executor._mutation_type).value
        if 'mutation_start' in state:
            del state['mutation_start']
        if 'mutation_end' in state:
            del state['mutation_end']
        if self.stack:
            last = self.stack[-1]
            if last.keyword == 'begin' and last.param == 'mutation':
                state['mutation_ignored'] = not last.data['type'] == _mutation_type
                state['mutation_start'] = True
                state['in_mutation'] = True
                state['mutation_id'] = self.createID(last, **kvargs)
                state['mutation_flavor'] = MutationFlavor.original
                state['mutation_type'] = last.data['type']
                self.stack.pop()
                print(info("Step into mutation declaration."))
                print(info("Step into original flavor."))
            elif last.keyword == 'end':
                if last.param == 'mutation':
#                    del state['mutation_ignored']
                    state['mutation_end'] = True
                    state['in_mutation'] = False
                    del state['mutation_flavor']
#                    del state['mutation_type']
#                    del state['mutation_id']
                    print(info("Leave mutation declaration."))
                    self.stack.pop()
                elif last.param == 'original':
                    state['mutation_flavor'] = MutationFlavor.modified
                    print(info("Leave original flavor."))
                    print(info("Step into modified flavor."))
                    self.stack.pop()


class DisableMutationAction(SodaAnnotationAction):
    def __init__(self, executor):
        super().__init__(executor)
        self.filter = MutationFilter.OnAll

    def Apply(self, line, state, **kvargs):
        _filter = CleverString(self.filter).value
        actOn = _filter == MutationFilter.OnAll or\
                 (_filter == MutationFilter.OnEnabled and not state.get('mutation_ignored', None)) or\
                 (_filter == MutationFilter.OnIgnored and state.get('mutation_ignored', None))
        if actOn:
            if state.get('mutation_flavor', None) == MutationFlavor.original:
                print(info("Emmit original source code line."))
                return line
            elif state.get('mutation_flavor', None) == MutationFlavor.modified:
                print(info("Suppress modified source code line."))
                return '//%s //pySoDA: disabled' % line


class CountMutationsAction(SodaAnnotationAction):
    def Apply(self, line, state, **kvargs):
        if self.stack:
            last = self.stack[-1]
            if last.keyword == 'begin' and last.param == 'mutation' and last.data['type'] == self._executor._mutation_type:
                state['mutation_index'] = state.get('mutation_index', -1) + 1


class EnableMutationAction(SodaAnnotationAction):
    def __init__(self, executor):
        super().__init__(executor)
        self._last_enabled_mutation = None
        self._enable_next_mutation = True

    def Apply(self, line, state, **kvargs):
        if not state.get('mutation_ignored', None):
            if state.get('mutation_start', False):
                if not hasDiff(state.get('mutation_id', None), self._last_enabled_mutation):
                    self._enable_next_mutation = True
                    print(info("Enable next mutation."))
            if state.get('mutation_end', False):
                if self._enable_next_mutation and hasDiff(state.get('mutation_id', None), self._last_enabled_mutation):
                    self._enable_next_mutation = False
                    print(info("Disable next mutation."))
                    self._last_enabled_mutation = state['mutation_id']
                    self._executor.enabled_mutation_id = self._last_enabled_mutation
                    print(info("Mark mutation '%s' as last enabled." % as_proper(state['mutation_id'])))

            if self._enable_next_mutation and hasDiff(state.get('mutation_id', None), self._last_enabled_mutation):
                if state.get('mutation_flavor', None) == MutationFlavor.original:
                    print(info("Suppress original source code line."))
                    return '//%s //pySoDA: disabled' % line
                elif state.get('mutation_flavor', None) == MutationFlavor.modified:
                    print(info("Emit modified source code line."))
                    return line
            else:
                if state.get('mutation_flavor', None) == MutationFlavor.original:
                    print(info("Emmit original source code line."))
                    return line
                elif state.get('mutation_flavor', None) == MutationFlavor.modified:
                    print(info("Suppress modified source code line."))
                    return '//%s //pySoDA: disabled' % line