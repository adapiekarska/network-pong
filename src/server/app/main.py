"""
Module containing entry point for the server program.
"""

from src.server.app import Server


def main():
    s = Server()
    s.start()


if __name__ == "__main__":
    main()
