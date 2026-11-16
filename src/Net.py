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

        self.mouse_down = False
        self.click = False

        #file stuff
        self.save_dir: str = None

        self.cursor = pygame.SYSTEM_CURSOR_ARROW
        self._last_cursor = None

    def update(self):
        self.cursor = pygame.SYSTEM_CURSOR_ARROW
        self.click = False
        self.events = pygame.event.get()
        self.dt = self.clock.tick(60) / 1000.0
        for event in self.events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1: 
                    self.mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP and self.mouse_down: 
                if event.button == 1: 
                    self.mouse_down = False
                    self.click = True

    def mouse_cursor(self):
        if self.cursor != self._last_cursor:
            pygame.mouse.set_cursor(self.cursor)
            self._last_cursor = self.cursor


Net = _Net()

