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

        self.fontSize = 46
        self.font = pygame.font.SysFont("consolas", self.fontSize)
        self.fontWidth = self.font.size("w")[0]

        self.code: list[CodeLine] = []
        self.gen()

        self.cursorTimer = Timer(0.5, True)
        self.cursorVis = False
        self.cursorIndex = 0
        self.cursory = 0
        self.cursorPos = [(55, 2), (55, self.code[-1].pan.dim.y)]

    def set_cursor_pos(self):
        #set line pos
        w = self.code[-1].pan.dim.y
        self.cursorPos = [
            (55+(self.fontWidth*self.cursorIndex), self.cursory*w),
            (55+(self.fontWidth*self.cursorIndex), (self.cursory*w)+w),
        ]

    def update_cursor_vis(self):
        self.cursorTimer.update()
        if self.cursorTimer.done:
            self.cursorVis = not self.cursorVis
            self.cursorTimer.start()

    def cursor_navigation(self, line: CodeLine, index: int):
        # arrow keys (up / down)
        if Keys.is_pressed(Keys.up): dir = -1
        elif Keys.is_pressed(Keys.down): dir = 1
        else: dir = 0
        if (dir < 0 and index > 0) or (dir > 0 and index < len(self.code) - 1):
            line.set_active(False)
            self.code[index + dir].set_active(True)
            self.cursory = index + dir
            self.cursorVis = True
            self.cursorTimer.start()

    def _update_cursor(self, i):
        if i is None: 
            self.cursorVis = False
            return
        else: self.cursory = i
        line: CodeLine = self.code[i]
        if Net.click:
            self.cursorVis = True
            self.cursorTimer.start()
            #set pos
            w = round((line.pan.sub.local_mouse_pos().x - 55) / self.fontWidth)
            if w > len(line.text.text): self.cursorIndex = len(line.text.text)
            else: self.cursorIndex = w

        self.update_cursor_vis()
        self.cursor_navigation(line, i)
        self.set_cursor_pos()

    def gen(self):
        self.code.clear()
        #test
        y = 0
        for i in range(5):
            self.code.append(self.pan.add_object(CodeLine(y, self.pan, i+1, self.name, self._type, self.font, self.fontSize, Project)))
            y+=self.code[-1].pan.dim.y
        self.pan.add_object(Rect(0, 0, self.pan.dim.x, self.pan.dim.y, (0, 0, 0), 2))

    def update(self):
        active = None
        for line in self.code:
            line.update(self.cursorIndex)
            if line.active: 
                active=self.code.index(line)
                self.cursorIndex = line.i

        self._update_cursor(active)

    def render(self, screen):
        self.pan.render(render_sub=False)

        #cursor
        if self.cursorVis: pygame.draw.line(self.pan.sub.screen, "white", *self.cursorPos, width=2)
        
        self.pan.sub.render()


