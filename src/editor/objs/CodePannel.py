import pygame
import os
from PyScene import Vector2D

from ...Net import Net, _project
from ...utils import *

from .CodeLine import CodeLine

Project: _project = None

class CodePannel:
    def __init__(self, x, y, w, h, name, _type, project, pan: Pannel):
        global Project
        Project = project

        self.pos = Vector2D(x, y)
        self.dim = Vector2D(w, h)
        self.pan = Pannel(x, y, w, h, (18, 19, 20), "black", 5, displaySurface=pan.sub.screen, parent=pan.sub)

        self.name = name
        self._type = _type

        self.code: list[CodeLine] = []
        self.gen()

    def gen(self):
        self.code.clear()
        #test
        y = 0
        for i in range(150):
            self.code.append(self.pan.add_object(CodeLine(y, self.pan, i+1, self.name, self._type)))
            y+=self.code[-1].pan.dim.y
        self.pan.add_object(Rect(0, 0, self.pan.dim.x, self.pan.dim.y, (0, 0, 0), 2))

    def update(self):
        for line in self.code:
            line.update()

    def render(self, screen):
        self.pan.render()

