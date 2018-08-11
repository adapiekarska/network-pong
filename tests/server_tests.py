"""
Tests for server functionalities.
"""

from client import Client
from server import server_config
from server.server_main import Server
from client.client_main import Client

def test_maximum_capacity():
    s = Server()
    clients = [Client() for _ in range(server_config.MAX_GAMES*2)]
    for c in clients:
        c.connect_to_server()
