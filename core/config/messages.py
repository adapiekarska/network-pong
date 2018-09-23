"""
Module containing all possible messages that can be shared between instances
of server and clients. It stores byte messages in a private dictionary, and
ensures easy and safe access to them by providing function to get raw byte
message from the private dictionary given its name.
"""

from core.utils.exc import UnrecognizedVariableError


# Dictionary of all available messages. Every message should be as short
# and descriptive as possible. Storing messages in the dictionary
# provides easy and safe way of getting wanted message by simply
# calling get(name) function from this module with a name parameter,
# where 'name' must be an existing dictionary key.
_messages = {
    "MSG_CON_REQ": b'REQ',
    "MSG_IN": b'IN',
    "MSG_SERVER_FULL": b'FULL',
    "MSG_IDLE": b'IDLE',
    "MSG_ACK": b'ACK',
    "MSG_START": b'START'
}


def get(name):
    """Get message by its name.

    Get raw byte string message given its name.

    Args:
        name (str): name of the message. Must be a valid key contained in
            a private dictionary.

    Returns:
        A byte string value stored under the given key in the _messages
        dictionary

    Raises:
        core.utils.exc.UnrecognizedVariableError: if the name of the
        message is not contained in the private messages dictionary
    """

    if name in _messages:
        return _messages[name]
    else:
        raise UnrecognizedVariableError(name)
