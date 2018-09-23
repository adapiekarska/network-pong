"""
Module containing ConnectionManager class, which takes care of the connection
after it has been established in the earlier stage, and maintains it throughout
the entire duration of the session. ConnectionManager runs as a separate thread
in the client program.
"""


from threading import Thread
import time

from game_client import conf
from core.utils.net_utils import send


class ConnectionManager(Thread):
    """Class responsible for managing the connection.

    Class that takes care of the communication with the server after the connection
    has been established. Must be created and used after the ConnectionEstablisher
    succeeds in connecting. Extends threading.Thread.
    """

    def __init__(self, sock):
        """Constructor.

        Performs basic initialization.

        Args:
            sock (socket.socket): open UDP socket that was used to establish the connection
        """

        super(ConnectionManager, self).__init__()
        self._sock = sock

        self._server_address = conf.SERVER_ADDRESS
        self._server_port = conf.SERVER_PORT

        self._server_ep = (self._server_address, self._server_port)

    def run(self):
        """Main function of the ConnectionManager class.

        Manage the connection. This basically comes down to two main tasks: regularly
        notifying the server that the client is still connected and receiving the
        server's orders in the meantime. The 'IDLE' message is being sent to the client
        every few seconds.
        """

        while True:
            send(self._sock, "MSG_IDLE", self._server_ep)
            time.sleep(10)