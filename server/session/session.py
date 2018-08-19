"""
Module containing Session class for the server as well as game managing utilities.
"""

from threading import Thread


class Session(object):
    """
    Class representing a session. The session is a single established and
    ongoing connection between two remote players.
    """

    def __init__(self, c1, c2):
        """
        Session class constructor.
        :param tuple (string address, int port) c1: client 1
        :param tuple (string address, int port) c2: client 2
        """
        self._c1 = c1
        self._c2 = c2

    def game_func(self):
        pass

    def start(self):
        game_thread = Thread(target=self.game_func)