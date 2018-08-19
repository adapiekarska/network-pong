"""
Module containing exceptions raised in various scenarios during
execution of both client and server programs.
"""


class VariableNotSettableError(Exception):
    """
    Raised when the configuration variable, which is not marked as
    settable is being set.
    """
    def __init__(self, *args):
        super(VariableNotSettableError, self).__init__(*args)


class UnrecognizedVariableError(KeyError):
    """
    Raised when during the access to a configuration variable a
    wrong name is provided.
    """
    def __init__(self, *args):
        super(UnrecognizedVariableError, self).__init__(*args)


class ServerUnreachableError(Exception):
    """
    Raised in a situation when the server cannot be reached due
    to any reason.
    """
    def __init__(self, *args):
        super(ServerUnreachableError, self).__init__(*args)


class ProtocolError(Exception):
    """
    Raised when any one of the parties observes that the other one
    does not follow the protocol.
    """
    def __init__(self, *args):
        super(ProtocolError, self).__init__(*args)
