import pygame
import os

from PyScene import Vector2D

from ...Net import Net, _project
from ...utils import *


Project: _project = None

class SceneTopBar:
    def __init__(self, pan: Pannel):
        self.height = 50
        self.pan = Pannel(0, 5, pan.dim.x, self.height, (18, 19, 20), displaySurface=pan.sub.screen, parent=pan.sub)
        t = self.pan.add_object(Text(45, "Mode (f2):", "white", Vector2D(5, self.height//2), "midleft"))
        r = self.pan.sub.get_global_rect(pygame.Rect(t.rect.width+10, 5, self.height-10, self.height-10))
        self.toggle = self.pan.add_object(btn(t.rect.width+10, 5, self.height-10, self.height-10, (18, 19, 20), borderColor="white", 
                                              minw=2, maxw=0, toggle=True, toggleRect=r, sub=self.pan.sub))

    def update(self):
        self.toggle.update()

    def render(self, screen):
        self.pan.render()

