import socket

from core.config import server_data
from core.config import messages
from core.net_utils import send, receive
from core import exc

from server import server_config
from server.game.game import Game


class Server(object):
    """
    Main class for server program.
    """
    def __init__(self):
        """
        Constructor for Server class.
        """
        # initial global config setting
        server_data.set("SERVER_ADDRESS", server_config.SERVER_ADDRESS)
        server_data.set("SERVER_PORT", server_config.SERVER_PORT)

        # local setting
        self._address = server_data.get("SERVER_ADDRESS")
        self._port = server_data.get("SERVER_PORT")

        # create and bind a UDP socket
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Server started on {} port {}".format(self._address, self._port))
        self._sock.bind((self._address, self._port))

        # create a list of clients
        self._clients = []

        # create a list of active connections
        self._connections = []

    def _anyone_waiting(self):
        """
        Checks if there is someone waiting for the second player to start the game.
        :return: None if there is no one waiting. Otherwise, two values are returned:
        the index of a connection in connections list and the waiting client
        endpoint data.
        """
        for pair in self._connections:
            if pair[0] is -1:
                return self._connections.index(pair), self._clients[pair[1]]
            if pair[1] is -1:
                return self._connections.index(pair), self._clients[pair[0]]
        return None

    def listen_for_new_connections(self):
        print("current clients")
        print(self._clients)
        print("current connections")
        print(self._connections)
        print("waiting for any message")
        data, new_client_ep = receive(self._sock)
        print('received %s bytes from %s' % (len(data), new_client_ep))
        print(data)

        # if this is the first time the client connects
        if new_client_ep not in self._clients:
            # add the newly connected client to the list
            self._clients.append(new_client_ep)

            try:
                if data == messages.get("MSG_CON_REQ"):
                    other_in = self._anyone_waiting()
                    if other_in:
                        print("two players already in, game is ready")
                        conn_ind, other_ep = other_in
                        self._connections[conn_ind] = (self._clients.index(other_ep), self._clients.index(new_client_ep))
                        # notify two 'connected' players that they're in
                        send(self._sock, "MSG_IN", other_ep, new_client_ep)

                        # create new game including two newly matched players
                        game = Game(other_ep, new_client_ep)

                        # start new game as a separate thread on server
                        game.start()
                    else:
                        # accept connection only if the server is not full
                        if len(self._connections) < server_config.MAX_GAMES:
                            print("one player connected, waiting for other")
                            self._connections.append((self._clients.index(new_client_ep), -1))
                        else:
                            print("server is full")
                            send(self._sock, "MSG_SERVER_FULL", new_client_ep)
                else:
                    # incorrect situation
                    print("client not following protocol, denying")
                    raise exc.UnrecognizedMessageError
            except exc.UnrecognizedMessageError as err:
                print(err.__str__())

    def run(self):
        """
        Run the server's main loop.
        """
        while True:
            self.listen_for_new_connections()


def main():
    s = Server()
    s.run()


if __name__ == "__main__":
    main()
