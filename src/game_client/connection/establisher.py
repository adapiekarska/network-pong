"""
Module containing ConnectionEstablisher class, which is responsible for
instantiating connection to the server by performing a three-way handshake
with it.
"""


import socket

from src.core.utils.net_utils import send, receive
from src.core.config import messages
from src.core.utils import exc
from src.game_client import conf as CONFIG


class ConnectionEstablisher(object):
    """Class implementing connection establishment logic.

    The class is responsible for establishing the connection to the server,
    and the session with another remote machine via the server.
    """

    def __init__(self):
        """Constructor.

        Performs basic initialization of variables and opens a UDP socket.

        Raises:
            SystemExit: if the UDP socket could not be opened.
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
        return self._sock

    def establish(self):
        """Establish connection to the server and to the other remote player.

        Tries to connect to the server by sending a request and waiting for a response.
        If the server does not respond immediately, it means that there is no waiting
        client on the server.
        If the server responds in a desirable way, the three-way handshake is performed.

        Returns:
            True if connection was successfully established, False otherwise.

        Raises:
            core.utils.exc.ServerUnreachableError: if there was no response from the
            server or the server was full.
            core.utils.exc.ProtocolError: if the message received from the server
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
