"""
Module containing network utilities shared by both client and server.
"""

from src.core.config import messages


def send(sock, msg_name, *recvs):
    """Send a message via UDP socket.

    Send a message to any number of recipients. Calls socket.sendto() function
    from the socket module.

    Args:
        sock (socket.socket): opened UDP socket
        msg_name (str): string value of the name of the message to send
        recvs: any number of endpoints (str address, int port) of the receivers
    """

    msg = messages.get(msg_name)
    for r in recvs:
        print("sending {} to {}".format(msg, r))
        sock.sendto(msg, r)


def receive(sock, size=1024):
    """Receive a message via UDP socket.

    Calls socket.recvfrom() function from the socket module.

    Args:
        sock (socket.socket): opened UDP socket
        size (int): number of bytes to receive, defaults to 1024

    Returns:
        A received message and the sender's endpoint data, represented
        by a tuple of address string and port integer value.
    """

    msg, sender = sock.recvfrom(size)
    print("Got {} from {}".format(msg, sender))
    return msg, sender
