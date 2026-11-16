import pygame
import os
import sys
from PyScene import Vector2D

class _Net:
    def __init__(self):
        self.screen: pygame.Surface = None
        self.screen_rect: pygame.Rect = None
        self.screen_size: Vector2D = None
        self.clock: pygame.time.Clock = None
        self.dt: float = None
        self.events = None

        #file stuff
        self.save_dir: str = None

    def update(self):
        self.events = pygame.event.get()
        self.dt = self.clock.tick(60) / 1000.0
        for event in self.events:
            if event.type == pygame.QUIT:
                sys.exit()

Net = _Net()

