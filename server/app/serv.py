"""
Main module for the Server class.
"""

import socket
import time

from core.config import messages
from core.utils.net_utils import send, receive

from server import conf, server_data
from server.session import Session
from server.client.connection import Connections
from server.client.client import Clients, Client


class Server(object):
    """Class representing the server.

    Class responsible for listening and managing clients. It handles their first
    connections, establishes and runs session for each pair and keeps track of
    whether any of the clients is still connected and active. In other words, the
    Server class handles all communication protocols not directly connected with
    a particular session, but rather with establishing it.
    """

    def __init__(self):
        # initial global config setting
        server_data.set("SERVER_ADDRESS", "127.0.0.1")
        server_data.set("SERVER_PORT", conf.SERVER_PORT)
        server_data.set("MAX_CONNECTIONS", conf.MAX_CONNECTIONS)
        server_data.set("MAX_CLIENT_IDLE", conf.MAX_CLIENT_IDLE)

        # local setting
        self._address = server_data.get("SERVER_ADDRESS")
        self._port = server_data.get("SERVER_PORT")

        # create and bind a UDP socket
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Server started on {} port {}".format(self._address, self._port))
        self._sock.bind((self._address, self._port))

        self._clients = Clients()

        self._connections = Connections()

    def _clean_up(self):
        self._sock.close()

    def start(self):
        """Start the server.

        Run the pong_server's main loop. There are two main tasks that the server does
        during this function. First, it listens for incomming messages, then handles them
        accordingly to their contents, and after that, it checks whether any of the
        currently connected clients has disconnected.
        """
        while True:
            self._listen()
            self._inspect_clients()

    def stop(self):
        """Stops the execution of a server by raising SystemExit.
        """
        self._clean_up()
        raise SystemExit

    def _listen(self):
        """Listen for incoming messages and handle them properly according to their purpose.
        """

        print([c.ep for c in self._clients])
        print(self._connections)

        data, new_client_ep = receive(self._sock)

        # To treat incoming connection as a new client, two conditions must be met:
        # 1 - the client cannot be in already connected clients list,
        # 2 - the message that the client has sent should be the connection request message
        prev = self._clients.find_by_ep(new_client_ep)
        if prev:
            if data == messages.get("MSG_IDLE"):
                prev._last_idle = time.time()
        else:
            if data == messages.get("MSG_CON_REQ"):
                new_client = Client(new_client_ep)
                print("new_client", new_client)
                self._handle_new_client(new_client)

    def _inspect_clients(self):
        """Check current state for all connected clients.

        Run through the list of currently connected clients and check whether they have been
        active or not. If not, remove them from the list of currently connected clients.
        """
        print("checking clients, no of clients: {}".format(len(self._clients)))
        now = time.time()
        for c in self._clients:
            if c.last_idle != -1:
                print('last idle', now - c.last_idle)
                if now - c.last_idle > conf.MAX_CLIENT_IDLE:
                    self._remove_client(c)

    def _server_full(self):
        """Check if the server is full.

        Check whether the maximum capacity of the server has been reached, i.e. any new
        client cannot be accepted. Maximum number of concurrent connections can be specified
        in server_config.py file

        Returns:
            True if pong_server is full, False otherwise
        """
        return len(self._connections) >= server_data.get("MAX_CONNECTIONS")

    def _remove_client(self, client):
        """Remove client.

        Remove client from the list of currently connected clients and from the list of
        active connections.

        Args:
            client: client to remove from the server
        """
        for connection in self._connections:
            print(type(connection))
            if client in connection:
                connection.remove_client(client)

        self._clients.remove(client)

    def _handle_new_client(self, new_client):
        """Handle new client.

        Handle new client according to their current status and message that they send.

        Args:
            new_client: newly connected client
        """

        if not self._server_full():
            self._clients.append(new_client)

            result = self._connections.add_client(new_client)

            if result:
                c1, c2 = result
                if self._arrange_for_session(c1, c2):
                    session = Session(c1, c2)
                    session.start()
                    print('sending START')
                    send(self._sock, "MSG_START", c1.ep, c2.ep)
                else:
                    # the game could not be started due to the disconnection of one
                    # of the players
                    print("the game could not be started.")
            else:
                # there is no pair for the newly connected client, therefore it
                # has to wait
                pass
        else:
            # the server was full
            send(self._sock, "MSG_SERVER_FULL", new_client.ep)

    def _arrange_for_session(self, c1, c2):
        """Arrange the new session.

        Prepare for a new game to be started. Perform something like three-way handshake,
        i.e. first the server sends the message to clients notifying them that they
        are in, then both clients have to respond with ACK message, and if that happens,
        the server sends the confirmation message to both clients. After that, the
        connection between two clients is considered established.

        Args:
            c1: first client
            c2: second client

        Returns:
            True if the preparations succeeded, False otherwise
        """

        send(self._sock, "MSG_IN", c1.ep, c2.ep)
        try:
            msg_1, sender_1 = receive(self._sock)
            msg_2, sender_2 = receive(self._sock)

            conditions = messages.get("MSG_ACK") == msg_1 and messages.get("MSG_ACK") == msg_2 and \
                         ((sender_1, sender_2) == (c1.ep, c2.ep) or ((sender_1, sender_2) == (c2.ep, c1.ep)))

            return conditions

        except socket.error:
            # if the receive function above failed and the exception occurred, it means
            # that one of the clients closed its socket and probably sent the ICMP packet
            # that caused an error while receiving data.
            msg_2, c2 = receive(self._sock)
            disconnected = self._connections.get_pair_of(c2)

            self._remove_client(disconnected)

            print("clients: ", self._clients)
            print("connections: ", self._connections)
            return False
