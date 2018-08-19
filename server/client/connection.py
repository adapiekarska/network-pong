"""
Module containing Connection and Connections classes.
"""


class Connection(object):
    """
    Class representing single connection.
    """
    def __init__(self, c1, c2=None):
        """
        Constructor of the Connection class.
        If c2 parameter is not supplied, the Connection is instantiated as a one-end
        connection, meaning that there is one client waiting for some other to join
        him. This is represented by a tuple of server.client.client.Client and None.
        :param c1: first client
        :param c2: (optional) second client
        :type c1: server.client.client.Client
        :type c2: server.client.client.Client
        """
        self._c1 = c1
        self._c2 = c2

    def __contains__(self, key):
        """
        Makes usage of the 'in' keyword possible with the Connection object.
        :param key: key to look for in the Connection object
        :type key: server.client.client.Client or None
        :return: True if found, False otherwise
        :rtype: bool
        """
        return key == self._c1 or key == self._c2

    def other(self, c):
        """
        Given one of the parties of the connection, get the other one.
        :param c: given party
        :type c: server.client.client.Client or None
        :return: other party from the Connection
        :rtype: server.client.client.Client or None
        """
        return self._c1 if c == self._c2 else self._c2

    def remove_client(self, c):
        """
        Remove the client from the connection by placing None at its place.
        :param c: client to remove from the connection
        :type c: server.client.client.Client
        :raises ValueError: if the given client is not present in the connection.
        """
        if self._c1 == c:
            self._c1 = None
        elif self._c2 == c:
            self._c2 = None
        else:
            raise ValueError("{} not in connection".format(c))


class Connections(list):
    """
    Class representing list of connections between clients. Connections are stored
    as server.client.connection.Connection objects. There should not be more than
    one one-end connection in the Connections list at once. This is considered as
    improper behaviour.
    Extends list type.
    """
    def __init__(self):
        """
        Constructor for the Connections class.
        """
        super(Connections, self).__init__()

    def append(self, x):
        """
        Disable calling the regular append method, since the addition of new clients
        should happen through the add_client() method.
        """
        raise NotImplementedError

    def _append(self, x):
        """
        Append new entry to the list of connections. The argument to append must
        be an instance of the Connection class. This is an internal function
        only called by a public interface of add_client() method.
        :param x: entry to append
        :type x: server.client.client.Connection
        :raises TypeError: if the argument x does not have a valid type.
        """
        if not isinstance(x, Connection):
            raise TypeError("{} is not valid object", type(x))

        super(Connections, self).append(x)

    def add_client(self, client):
        """
        Add new pong_client to the list of connections, either by creating new one-end
        connection for that particular cilent and appending it to the list in regular way,
        or by matching the pong_client with some previously connected one, depending on
        whether there is some one-end connection present.
        :param client: client to add
        :type client: server.client.client.Client
        :return: tuple containing both of the newly connected players if the addition was
        performed by inserting the client into existing connection, None if the addition
        was performed by appending the new one-end connection to the list.
        :rtype: (server.client.client.Client, server.client.client.Client) or None
        """

        anyone_waiting = self._one_end_connection_present()
        if anyone_waiting:
            idx, other = anyone_waiting
            self[idx] = Connection(other, client)
            return other, client
        else:
            self._append(Connection(client))
            return None

    def get_pair_of(self, ep):
        """
        Get a pair of the client with the given endpoint.
        :param ep: endpoint data of the client
        :type ep: (str, int)
        :return: other client from the connection pair containing the client with the given
        endpoint
        :type: server.client.client.Client
        :raises ValueError: if no client with a given endpoint was found in active connections.
        """
        for connection in self:
            for c in connection:
                if c.ep == ep:
                    return connection.other(c)

        raise ValueError("Client with endpoint: {} not found in active connections list".format(ep))

    def _one_end_connection_present(self):
        """
        Check if there is someone waiting for the second player to start the game.
        Private function, not meant to be used outside the class.
        :return: None if there is no one-end connection in the active connections list,
        otherwise tuple of two values is returned: the index of the first connection
        with only one end and the other waiting client from that pair
        :rtype: (int, server.client.client.Client) or None
        """
        for i, connection in enumerate(self):
            if None in connection:
                return i, connection.other(None)

        return None