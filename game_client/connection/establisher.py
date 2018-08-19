"""
Module containing ConnectionEstablisher class, which is responsible for
instantiating connection to the server by performing a three-way handshake
with it.
"""


import socket

from core.utils.net_utils import send, receive
from core.config import messages
from core.utils import exc
from game_client import conf as CONFIG


class ConnectionEstablisher(object):
    """
    Class implementing connection establishment logic.
    """

    def __init__(self):
        """
        Performs basic initialization of variables and opens a UDP socket.
        :raises SystemExit: if the UDP socket could not be opened
        """

        self._address = "127.0.0.1"

        self._server_address = CONFIG.SERVER_ADDRESS
        self._server_port = CONFIG.SERVER_PORT

        self._server_ep = (self._server_address, self._server_port)

        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sock.bind((self._address, 0))
        except socket.error as err:
            print(err.__str__())
            raise SystemExit

    @property
    def sock(self):
        """
        Getter method for a socket variable.
        :return: socket object.
        """
        return self._sock

    def establish(self):
        """
        Tries to connect to the server by sending a request and waiting for a response.
        :return: True if connection was successfully established, False otherwise.
        :raises core.utils.exc.ServerUnreachableError: if there was no response from the
        server or the server was full.
        :raises core.utils.exc.ProtocolError: if the message received from the server
        was not recognized as the valid message.
        """

        send(self._sock, "MSG_CON_REQ", self._server_ep)
        try:
            result = receive(self._sock)
        except socket.error:
            raise exc.ServerUnreachableError("Connection to {} on port {} could not be established."
                                             .format(self._server_address, self._server_port))

        response, server = result

        # Three-way handshake
        if response == messages.get("MSG_IN"):
            send(self._sock, "MSG_ACK", self._server_ep)
            response, server = receive(self._sock)
            if response == messages.get("MSG_START"):
                return True
        elif response == messages.get("MSG_SERVER_FULL"):
            raise exc.ServerUnreachableError("Server denied the connection due to the overfill.")
        else:
            raise exc.ProtocolError("Server not following protocol. Got {}.".format(response))

        return False
