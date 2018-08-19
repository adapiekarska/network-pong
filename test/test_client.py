import pytest

from game_client import Client

# TODO how to test both client and server with their blocking methods in the same script?


def test_client():
    with pytest.raises(SystemExit):
        c = Client()
        c.start(False)
