"""
Module containing all necessary pre-configuration utilities for the server.
Notice that no assignment of values takes place here. This module only
provides utilities needed for any such assignment to take place.
You should not make any changes to this code if you want to change the
pong_server configuration, because your changes would still be overwritten.
"""

from src.core.utils import exc

_server_data = {
    "SERVER_ADDRESS": "",
    "SERVER_PORT": "",
    "MAX_CONNECTIONS": "",
    "MAX_CLIENT_IDLE": ""
}

_writable = [
    "SERVER_ADDRESS",
    "SERVER_PORT",
    "MAX_CONNECTIONS",
    "MAX_CLIENT_IDLE"
]


def get(name):
    """
    Get data from private dictionary given its name.

    Args:
        name: key from the private dictionary under which the wanted value
    is stored

    Return:
        value stored in a private dictionary under the given key
    """
    return _server_data[name]


def set(name, value):
    """
    Set specific server configuration parameter to a given value.

    Args:
        name: the name of the parameter (key from _server_data dictionary)
        value: value to be set

    Raises:
        exc.VariableNotSettableError: if the parameter that you want to set
    was not configured to be writable.
        exc.UnrecognizedVariableError: if the name is not contained in the
    private dictionary
    """
    if name in _server_data:
        if name in _writable:
            _server_data[name] = value
        else:
            raise exc.VariableNotSettableError("{} not settable".format(name))
    else:
        raise exc.UnrecognizedVariableError("{} is not a valid variable name".format(name))
