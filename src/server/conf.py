"""
User configuration file for the server.
If you want to change the configuration of the server, this is the right place to do so.
"""

"""
Server endpoint configuration.
"""
SERVER_PORT = 50000

"""
Maximal amount of concurrent connections. A connection here means the connection between
two remote clients, not the connection from one client to the server.
"""
MAX_CONNECTIONS = 3

"""
Maximal amount of time that must have elapsed for the client to be considered inactive
(in seconds).
"""
MAX_CLIENT_IDLE = 15
