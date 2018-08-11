"""
Module containing Game class for server as well as game managing utilities.
"""

from threading import Thread

class Game(object):
    """
    Class representing single game between two remote players.
    """

    def __init__(self, p1, p2):
        """
        Game class constructor.
        :param tuple (string address, int port) p1: player 1
        :param tuple (string address, int port) p2: player 2
        """
        self._p1 = p1
        self._p2 = p2

    def game_func(self):
        print("game thread: players: {1}, {2}".format(self._p1, self._p2))

    def start(self):
        print("game started")
        game_thread = Thread(target=self.game_func)