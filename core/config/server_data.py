# TODO how to move this to __init__.py
from core.exc import VariableNotSettableError

"""
Module containing all necessary pre-configuration utilities for server.
Note: you should not make any changes to this code if you want to change the
server configuration, because it will still be overwritten.
"""

_server_data = {
    "SERVER_ADDRESS": " ",
    "SERVER_PORT": " "
}
_writable = ["SERVER_ADDRESS", "SERVER_PORT"]


def get(name):
    return _server_data[name]


def set(name, value):
    if name in _writable:
        _server_data[name] = value
    else:
        raise VariableNotSettableError("Error: {} not settable".format(name))