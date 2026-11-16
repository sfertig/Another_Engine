import pygame
from PyScene import Vector2D

from ..utils import *
from ..Net import Net

class ProjectManager:
    def __init__(self):
        pygame.quit() # <- if editor was running
        pygame.init()

        #screen and basics
        Net.screen_size = Vector2D(1024, 600)
        Net.screen = pygame.display.set_mode(Net.screen_size.to_int())
        pygame.display.set_caption("AnotherEngine Project Manager")
        Net.screen_rect = Net.screen.get_rect()
        Net.clock = pygame.time.Clock()
        Net.dt = 0.0

        #test
        self.topBar = Pannel(0, 0, Net.screen_size.x, 30, [29, 34, 41], (0, 0, 0), 2, Net.screen)
        self.topBar.add_object(Text(35, "Project Manager", (255, 255, 255), Vector2D(10, 5), "topleft"))

    def Run(self):
        while True:
            Net.update()
            self.update()
            self.render()

    def update(self):
        pass

    def render(self):
        Net.screen.fill((0, 0, 0))

        self.topBar.render()

        Net.mouse_cursor()
        pygame.display.flip()
