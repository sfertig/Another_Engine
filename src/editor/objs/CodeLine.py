import pygame
import os
from PyScene import Vector2D

from ...Net import Net, _project
from ...utils import *

Project: _project = None

class CodeLine:
    def __init__(self, y, pan: Pannel, num, name, _type, font, fontSize, project):
        global Project
        Project = project

        self.pos = Vector2D(0, y)
        self.pan = Pannel(self.pos.x, y, pan.dim.x-self.pos.x, fontSize+4, (18, 19, 20), displaySurface=pan.sub.screen, parent=pan.sub)
        self.num = num
        self.name = name
        self._type = _type

        #test / debug
        self._num = self.pan.add_object(btn(-50, 0, 100, fontSize+4,(18, 19, 20), str(num), font=font, sub=pan.sub, TextAlign="midleft"))
        self.btn = btn(self.pos.x, y, pan.dim.x, fontSize+4, "black", sub=pan.sub, toggle=True, toggleSelf=False)

        self.fntS = fontSize
        self.text = self.pan.add_object(Text(font, self.get_line(num-1), "white", Vector2D(55, self.pan.dim.y//2), "midleft"))

        self.active = False

    def set_active(self, state):
        self.btn.pressed = state
        self.chech_active()

    def chech_active(self):
        self.active = self.btn.update()
        if self.active: self.pan.sub.color = (36, 37, 38)
        else: self.pan.sub.color = (18, 19, 20)

    def input(self, index):  # index of the cursor
        if Keys.is_held(Keys.control): return index
        text = self.text.text
        for event in Net.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if index > 0:
                        text = text[:index - 1] + text[index:]
                        index -= 1
                elif event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    continue
                elif event.key == pygame.K_TAB:
                    text = text[:index] + " "*4 + text[index:]
                    index += 4
                else:
                    if event.unicode:  # Prevents non-printable keys (like Shift) from moving the cursor
                        text = text[:index] + event.unicode + text[index:]
                        index += len(event.unicode)

        if text != self.text.text: self.text.set_text(text)
        return index


    def update(self, index: int):
        self.chech_active()
        if not self.active: return

        self.i = self.input(index)
        self.set_line()


    def render(self, screen):
        self.pan.render()

    def set_text(self, text):
        self.text.set_text(text)
        self.set_line()

    def set_y(self, y):
        self.pan.pos.y = y
        self.pos.y = y
        self.pan.sub.pos.y = y

    def set_num(self, num):
        self.num = num
        self._num.text.set_text(str(num))

    def get_line(self, lineIndex):
        code: list[str] = getattr(Project, self._type+"s")[self.name]["code"]
        if lineIndex <= len(code)-1: return getattr(Project, self._type+"s")[self.name]["code"][lineIndex]
        else: 
            getattr(Project, self._type+"s")[self.name]["code"].append("")
            return ""


    def set_line(self):
        text = getattr(Project, self._type+"s")[self.name]["code"][self.num-1]
        if text != self.text.text: 
            #print("modified")
            getattr(Project, self._type+"s")[self.name]["changed"] = True
            getattr(Project, self._type+"s")[self.name]["dirty"] = True
            getattr(Project, self._type+"s")[self.name]["code"][self.num-1] = self.text.text

