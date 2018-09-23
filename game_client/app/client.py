"""
Module containing main class for the client program.
"""

from game_client.connection import ConnectionEstablisher
from game_client.connection import ConnectionManager
from game_client.graphics import GraphicsManager

from core.utils import exc


class Client(object):
    """Class representing the client.

    This class handles all managers' initialization and startup.
    """

    def __init__(self):
        self._sock = None

    def start(self, graphics=True):
        """Start the client.

        Starts the client program. Instantiates connection with server and starts
        a graphic manager. Keeps the server connection throughout whole duration of the
        session.

        Args:
            graphics: boolean value that indicates whether the client should run with
            graphical user interface or only as a console application (useful for tests).

        Raises:
            SystemExit: if connection to server could not be established.
        """

        # Connect to the server.
        # This is done as a blocking operation, because there is no point in proceeding
        # to the game before client connects to the server
        ce = ConnectionEstablisher()

        try:
            if not ce.establish():
                raise SystemExit
        except exc.ServerUnreachableError as err:
            print(err)
            raise SystemExit

        self._sock = ce.sock

        cm = ConnectionManager(self._sock)
        cm.start()

        if graphics:
            with GraphicsManager() as gm:
                gm.mainloop()

        cm.join()

    def stop(self):
        """
        Exits the script by raising SystemExit.
        """
        self._clean_up()
        raise SystemExit

    def _clean_up(self):
        """
        Performs clean up.
        """
        self._sock.close()
