import pygame
import os
from PyScene import Vector2D

from ...Net import Net, _project
from ...utils import *

Project: _project = None

class CodeLine:
    def __init__(self, y, pan: Pannel, num, name, _type):
        self.pos = Vector2D(2, y)
        fontSize=46
        self.pan = Pannel(self.pos.x, y, pan.dim.x-self.pos.x*2, fontSize+4, (18, 19, 20), displaySurface=pan.sub.screen, parent=pan.sub)
        self.num = num
        self.name = name
        self._type = _type

        #test / debug
        self.pan.add_object(btn(-50, 0, 100, fontSize+4,(18, 19, 20), str(num), font=fontSize, sub=pan.sub, TextAlign="midleft"))
        self.btn = btn(self.pos.x, y, pan.dim.x, fontSize+4, "black", sub=pan.sub, toggle=True, toggleSelf=False)

        font = pygame.font.SysFont("consolas", fontSize)
        self.fntS = fontSize
        self.text = self.pan.add_object(Text(font, "", "white", Vector2D(55, self.pan.dim.y//2), "midleft"))

        self.cursorTimer = Timer(0.5, True)
        self.cursorVis = False
        self.cursorIndex = 0

        self.active = False

    def update_cursor_vis(self):
        self.cursorTimer.update()
        if self.cursorTimer.done:
            self.cursorVis = not self.cursorVis
            self.cursorTimer.start()

    def chech_active(self):
        was_active = self.active
        self.active = self.btn.update()
        
        if self.active != was_active:
            if self.active:
                self.pan.sub.color = (36, 37, 38)
                self.cursorVis = True
                self.cursorTimer.start()
            else:
                self.pan.sub.color = (18, 19, 20)
                self.cursorVis = False

        
    def update(self):
        self.chech_active()
        if not self.active: return
        self.update_cursor_vis()

    def render(self, screen):
        self.pan.render(render_sub=False)
        if self.active and self.cursorVis:
            pygame.draw.line(self.pan.sub.screen, "white", (55+(self.cursorIndex*self.fntS), 0), (55+(self.cursorIndex*self.fntS), self.pan.dim.y))
        self.pan.sub.render()

