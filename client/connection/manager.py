"""
Module containing ConnectionManager class.
"""


from threading import Thread
from core.config import server_data


class ConnectionManager(Thread):
    """
    Class that takes care of the communication with server after the connection has been established.
    Must be created and used after the ConnectionEstablisher succeeds in connecting.
    Extends threading.Thread.
    """
    def __init__(self, sock):
        """
        Perform basic initialization.
        :param socket sock: socket that was used to establish the connection.
        """
        super(ConnectionManager, self).__init__()
        self._sock = sock
        self._server_address = server_data.get("SERVER_ADDRESS")
        self._server_port = server_data.get("SERVER_PORT")

    def run(self):
        """
        """
        print("running connection manager's run method")