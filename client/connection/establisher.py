"""
Module containing ConnectionEstablisher class.
"""

import socket

from core.net_utils import send, receive
from core.config import messages
from core.config import server_data
from core import exc


class ConnectionEstablisher(object):
    """
    Class implementing connection establishment logic.
    """

    def __init__(self):
        """
        Performs basic initialization of variables and opens a UDP socket.
        """

        # initial global config setting
        server_data.set("SERVER_ADDRESS", "127.0.0.1")
        server_data.set("SERVER_PORT", 50000)

        # local setting
        self._server_address = server_data.get("SERVER_ADDRESS")
        self._server_port = server_data.get("SERVER_PORT")

        # open a socket
        self._open_socket()

    @property
    def sock(self):
        """
        Getter method for a socket variable.
        :return: socket object.
        """
        return self._sock

    def _open_socket(self):
        """
        Opens a UDP socket for communication with server. Private function,
        not meant to be called from outside of the class.
        """
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as err:
            print(err.__str__())

    def establish(self):
        """
        Tries to connect to a server by sending a request and waiting for a response.
        :return
        :raise
        """

        # send request for connection to the game
        print("sending request for connection to a game.")
        send(self._sock, "MSG_CON_REQ", (self._server_address, self._server_port))

        try:
            # check for response
            result = receive(self._sock)
            if result is None:
                return False
            response, server = result
            print('received %s bytes from %s' % (len(response), server))
            print(response)
            if response == messages.get("MSG_IN"):
                print("I'm in")
                return True
            elif response == messages.get("MSG_SERVER_FULL"):
                print("server is apparently full")
            else:
                raise exc.UnrecognizedMessageError
        except ConnectionResetError as err:
            print(err.__str__())
            raise SystemExit
        except exc.UnrecognizedMessageError as err:
            print(err.__str__())

        return False

