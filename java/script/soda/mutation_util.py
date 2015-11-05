class MutationFlavor:
    original = 'original'
    modified = 'modified'

class MutationType:
    none = 'none'
    returnType = 'return'
    ifType = 'if'
    variableSwitchType = 'variable_switch'
    statementDeletionType = 'statement_deletion'

class MutationFilter:
    OnAll = "all"
    OnIgnored = "ignored"
    OnEnabled = "enabled"