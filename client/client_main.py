"""
Module containing entrypoint class for the client program.
"""

from client.connection import ConnectionEstablisher
from client.connection import ConnectionManager
from client.graphics import GraphicsManager


class Client(object):
    """
    Main class for the client program.
    """

    def __init__(self):
        pass

    def start(self):
        """
        Starts the client program. Instantiates connection with server and graphical
        user interface manager. Keeps the server connection throughout whole program
        duration.
        """

        # Connect to the server.
        # This is done as a blocking operation, because there is no point
        # in proceeding before client connects to the server
        ce = ConnectionEstablisher()
        if not ce.establish():
            print("Connection could not be established.")
            raise SystemExit

        print("connection established")

        # create connection manager thread
        cm = ConnectionManager(ce.sock)
        cm.start()

        # instantiate graphics manager
        with GraphicsManager() as gm:
            gm.mainloop()

        # wait for connection manager thread to end
        cm.join()


if __name__ == "__main__":
    """
    Utility that is executed when run in command line.
    """
    npg = Client()
    npg.start()