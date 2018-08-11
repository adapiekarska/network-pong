from core.exc import UnrecognizedMessageError


_messages = {
    "MSG_CON_REQ": b'REQ',
    "MSG_IN": b'IN',
    "MSG_SERVER_FULL": b'FULL',
    "MSG_CLIENT_DISCONNECT": b'DIS'
}

def get(name):
    """
    Get message by its name.
    :param str name: name of the message
    :return: value of the message
    :rtype byte str
    :raises UnrecognizedMessageError: if the name of the message is not valid name
    """
    if name in _messages:
        return _messages[name]
    else:
        raise UnrecognizedMessageError
