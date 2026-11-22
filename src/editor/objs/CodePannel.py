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

    def handle_enter(self):
        line: CodeLine = self.code[self.cursory]
        line.set_active(False)
        # 1. Split the current line's text
        text = line.text.text  # adjust if you have a getter/setter on Text
        left_text = text[:self.cursorIndex]
        right_text = text[self.cursorIndex:]
        line.set_text(left_text)
        #add line
        y = (self.cursory+1)*self.code[0].pan.dim.y
        new_line = CodeLine(
            y, self.pan, line.num+1,
            self.name, self._type, self.font, self.fontSize, Project
        )
        new_line.set_active(True)
        new_line.set_text(right_text)
        self.code.insert(self.cursory + 1, new_line)
        self.pan.add_object(new_line)
        
        for idx, other_line in enumerate(self.code[self.cursory + 2:], start=self.cursory + 2):
            other_line.set_y(idx * self.code[0].pan.dim.y)
            other_line.set_num(idx + 1)

        self.cursory+=1
        self.cursorIndex = 0
        self.cursorVis = True
        self.cursorTimer.start()

    def handle_backspace(self):
        line: CodeLine = self.code[self.cursory]
        text = line.text.text

        # Case 1: Cursor is mid-line -> delete one character to the left
        if self.cursorIndex > 0:
            new_text = text[:self.cursorIndex - 1] + text[self.cursorIndex:]
            line.set_text(new_text)
            self.cursorIndex -= 1
            self.cursorVis = True
            self.cursorTimer.start()
            return

        # Case 2: Cursor is at start of line (cursorIndex == 0) and not on the first line -> merge up
        if self.cursory > 0:
            prev_line: CodeLine = self.code[self.cursory - 1]
            prev_text = prev_line.text.text

            # 1. Join current line's text onto the end of the previous line
            new_cursor_x = len(prev_text)
            prev_line.set_text(prev_text + text)
            prev_line.set_active(True)

            # 2. Remove the current line from self.code and self.pan
            self.code.pop(self.cursory)
            if hasattr(self.pan, "remove_object"):
                self.pan.remove_object(line)
            elif hasattr(self.pan, "objects") and line in self.pan.objects:
                self.pan.objects.remove(line)

            # 3. Shift all remaining lines below the merged line up
            line_height = self.code[0].pan.dim.y
            for idx, other_line in enumerate(self.code[self.cursory:], start=self.cursory):
                other_line.set_y(idx * line_height)
                other_line.set_num(idx + 1)

            # 4. Update cursor position and timer
            self.cursory -= 1
            self.cursorIndex = new_cursor_x
            self.cursorVis = True
            self.cursorTimer.start()


    def gen(self):
        self.code.clear()
        #test
        y = 0
        for i in range(len(getattr(Project, self._type+"s")[self.name]["code"])):
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
        if Keys.is_pressed(Keys.enter): self.handle_enter()
        elif Keys.is_pressed(Keys.backspace): self.handle_backspace()

    def render(self, screen):
        self.pan.render(render_sub=False)

        #cursor
        if self.cursorVis: pygame.draw.line(self.pan.sub.screen, "white", *self.cursorPos, width=2)
        
        self.pan.sub.render()


