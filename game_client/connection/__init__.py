"""
Package that includes connection establishment and management utilities for
the client program. It contains two modules: establisher.py and manager.py.
The establisher module contains definition of the ConnectionEstablisher class,
while the manager module contains definition of the ConnectionManager class.
The difference between the responsibilities of these two classes is mainly that
the ConnectionEstablisher class takes care of instantiating the connection,
making sure to follow the shared protocol, and the ConnectionManager handles
already established connection throughout the duration of the entire session.
"""

from game_client.connection.establisher import ConnectionEstablisher
from game_client.connection.manager import ConnectionManager
