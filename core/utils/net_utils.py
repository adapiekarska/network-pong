"""
Module containing network utilities shared by both client and server.
"""


from core.config import messages


def send(sock, msg_name, *recvs):
    """
    Send a message to any number of recipients. Calls socket.sendto() function
    from the socket module.
    :param sock: opened UDP socket
    :param msg_name: name of the message to send
    :param recvs: any number of endpoints (address, port) tuple of the receivers
    :type sock: socket.socket
    :type msg_name: str
    :type recvs: (str, int)
    """
    msg = messages.get(msg_name)
    for r in recvs:
        print("sending {} to {}".format(msg, r))
        sock.sendto(msg, r)


def receive(sock, size=1024):
    """
    Receive a message. Calls socket.recvfrom() function from the socket module.
    :param sock: opened UDP socket
    :param size: number of bytes to receive, defaults to 1024
    :type sock: socket.socket
    :type size: int
    :return: message and sender's endpoint data
    :rtype: (str received, (str, int))
    """
    msg, sender = sock.recvfrom(size)
    print("Got {} from {}".format(msg, sender))
    return msg, sender
