"""
Module containing graphics utilities.
"""

import pygame


class GraphicsManager(object):
    """
    Class handling graphical interface.
    """
    def __init__(self):
        """
        Constructor of the GraphicsManager class.
        """
        # initialize pygame module
        pygame.init()

        # set the surface size
        surface_size = (480, 480)
        self.surface = pygame.display.set_mode(surface_size)

        # set the window title
        pygame.display.set_caption("network-pong")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pygame.quit()

    def mainloop(self):
        # enter main game loop
        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                break

            self.surface.fill((0, 0, 0))
            self.surface.fill((255, 0, 0), (300, 100, 150, 90))
            pygame.display.flip()