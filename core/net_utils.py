from socket import error

from core.config import messages
from core.exc import UnrecognizedMessageError


def send(sock, msg_name, *recvs):
    """
    Send a message to any number of recipients.
    :param socket.socket sock: UDP socket
    :param byte str msg_name: name value of the message to send
    :param *recvs: any number of endpoints (address, port tuple)
    """
    try:
        msg = messages.get(msg_name)
    except UnrecognizedMessageError as err:
        print(err.__str__())

    for r in recvs:
        sock.sendto(msg, r)


def receive(sock, size=1024):
    """
    Receive a message.
    :param socket.socket sock: UDP socket
    :param int size: number of bytes to receive, default to 1024
    :return: received message, sender endpoint
    """
    try:
        msg, sender = sock.recvfrom(size)
        return msg, sender
    except error as err:
        print(err.__str__())
    except UnrecognizedMessageError as err:
        print(err.__str__())

    return None