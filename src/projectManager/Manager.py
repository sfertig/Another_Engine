import pygame
from PyScene import Vector2D

from ..utils import get_path
from ..Net import Net

class ProjectManager:
    def __init__(self):
        pygame.quit() # <- if editor was running

        #screen and basics
        Net.screen_size = Vector2D(1024, 600)
        Net.screen = pygame.display.set_mode(Net.screen_size.to_int())
        Net.screen_rect = Net.screen.get_rect()
        Net.clock = pygame.time.Clock()
        Net.dt = 0.0

    def Run(self):
        while True:
            Net.update()
            self.update()
            self.render()

    def update(self):
        pass

    def render(self):
        Net.screen.fill((0, 0, 0))

        pygame.display.flip()
