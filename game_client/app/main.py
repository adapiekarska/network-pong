"""
Module containing entry point for the client program.
"""


from game_client.app import Client


if __name__ == "__main__":
    """
    Console entry point for client program.
    """
    npg = Client()
    npg.start()
