"""
Module containing Client and Clients class.
"""


class Client(object):
    """
    Class representing single client connecting to the server.
    """
    def __init__(self, *args):
        """
        Constructor of the Client class. Can be called with various amount of arguments.
        There are two main options: either provide a tuple argument, containing client's
        address and port number, or specify address and port number through two distinct
        arguments.
        :param args: list of arguments
        """
        if isinstance(args[0], tuple):
            self._address = args[0][0]
            self._port = args[0][1]
        elif isinstance(args[0], str) and isinstance(args[1], int):
                self._address = args[0]
                self._port = args[1]

        self.last_idle = -1

    @property
    def ep(self):
        """
        Getter method for the client's endpoint data.
        :return: address, port
        :rtype: (str, int)
        """
        return self._address, self._port


class Clients(list):
    """
    Class representing the clients lists. Stores clients as a server.client.client.Client
    objects. Extends list type.
    """
    def __init__(self):
        """
        Constructor of the Clients class.
        """
        super(Clients, self).__init__()

    def find_by_ep(self, ep):
        """
        Find a client in the list knowing its endpoint data.
        :param ep: endpoint data of the client to find
        :type ep: (str, int)
        :return: client with the given endpoint, or None if none was found
        :rtype: server.client.client.Client or None
        """
        for element in self:
            if element.ep == ep:
                return element

        return None
