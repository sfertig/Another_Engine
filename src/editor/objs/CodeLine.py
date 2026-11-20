import pygame
import os
from PyScene import Vector2D

from ...Net import Net, _project
from ...utils import *

Project: _project = None

class CodeLine:
    def __init__(self, y, pan: Pannel, num, name, _type):
        self.pos = Vector2D(0, y)
        fontSize=46
        self.pan = Pannel(self.pos.x, y, pan.dim.x, fontSize+4, (18, 19, 20), displaySurface=pan.sub.screen, parent=pan.sub)
        self.num = num
        self.name = name
        self._type = _type

        #test / debug
        self.pan.add_object(btn(-50, 0, 100, fontSize+4,(18, 19, 20), str(num), font=fontSize, sub=pan.sub, TextAlign="midleft"))
        self.btn = btn(self.pos.x, y, pan.dim.x, fontSize+4, "black", sub=pan.sub, toggle=True, toggleSelf=False)

        self.active = False

    def chech_active(self):
        self.active = self.btn.update()
        if self.active: self.pan.sub.color = (36, 37, 38)
        else: self.pan.sub.color = (18, 19, 20)
        
    def update(self):
        self.chech_active()
    def render(self, screen):
        self.pan.render()

