"""
Module containing Client and Clients class.
"""


class Client(object):
    """
    Class representing single client connecting to the server.
    """
    def __init__(self, *args):
        """Constructor.

        Can be called with various amount of arguments.
        There are two main options: either provide a tuple argument, containing client's
        address and port number, or specify address and port number through two distinct
        arguments.

        Args:
            args: list of arguments
        """
        if isinstance(args[0], tuple):
            self._address = args[0][0]
            self._port = args[0][1]
        elif isinstance(args[0], str) and isinstance(args[1], int):
                self._address = args[0]
                self._port = args[1]

        self._last_idle = -1

    @property
    def ep(self):
        """Endpoint tuple."""
        return self._address, self._port


class Clients(list):
    """Class representing the clients lists.

    Stores clients as a server.client.client.Client objects.
    Extends list type.
    """

    def __init__(self):
        super(Clients, self).__init__()

    def find_by_ep(self, ep):
        """Find a client in the list knowing its endpoint data.
        Args:
            ep: endpoint data of the client to find

        Returns:
        client with the given endpoint, or None if none was found
        """
        for element in self:
            if element.ep == ep:
                return element

        return None
