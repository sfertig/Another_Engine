import pygame
import os
from PyScene import Vector2D

from ...Net import Net, _project
from ...utils import *

from .CodeHilighter import CodeHighlighter

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
        self._num = self.pan.add_object(btn(-50, 0, 100, fontSize+4,(18, 19, 20), str(num), font=font, sub=pan.sub, TextAlign="midleft", textColor=(133, 136, 137)))
        self.btn = btn(self.pos.x, y, pan.dim.x, fontSize+4, "black", sub=pan.sub, toggle=True, toggleSelf=False)

        self.fntS = fontSize
        self.text = self.pan.add_object(Text(font, self.get_line(num-1), "white", Vector2D(55, self.pan.dim.y//2), "midleft"))

        self.active = False
        self.DIRTY = False
        self.highlighter = CodeHighlighter()
        self.highlight()

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
                    continue
                    """if index > 0:
                        text = text[:index - 1] + text[index:]
                        index -= 1"""
                elif event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    continue
                elif event.key == pygame.K_TAB:
                    text = text[:index] + " "*4 + text[index:]
                    index += 4
                else:
                    if event.unicode:  # Prevents non-printable keys (like Shift) from moving the cursor
                        c = event.unicode
                        if c == "\"": c+="\""
                        elif c == "\'": c+="\'"
                        elif c == "(": c+=")"
                        elif c == "[": c+="]"
                        elif c == "{": c+="}"
                        text = text[:index] + c + text[index:]
                        index += len(event.unicode)

        if text != self.text.text: 
            self.text.set_text(text)
            self.DIRTY = True
        return index


    def update(self, index: int):
        #self.DIRTY = False
        self.chech_active()
        if not self.active: return

        self.i = self.input(index)
        #self.set_line()


    def render(self, screen):
        self.pan.render()

    def set_text(self, text):
        self.text.set_text(text)
        self.DIRTY = True
        #self.set_line()

    def set_y(self, y):
        self.pan.pos.y = y
        self.pos.y = y
        self.pan.sub.pos.y = y
        self.btn.set_y(y)

    def set_num(self, num):
        self.num = num
        self._num.text.set_text(str(num))

    def _get_object_data(self):
        """Helper to fetch the object dictionary from Project safely."""
        return getattr(Project, self._type + "s")[self.name]

    def get_line(self, line_index: int) -> str:
        """
        Safely retrieves a line of code. Pads the list with empty strings 
        if the requested line index doesn't exist yet, keeping Project as the source of truth.
        """
        obj_data = self._get_object_data()
        code: list[str] = obj_data.setdefault("code", [])
        
        # Pad the list dynamically if index is out of bounds
        while len(code) <= line_index:
            code.append("")
            
        return code[line_index]

    def set_line(self):
        """
        Safely updates a line of code in the Project data store.
        Uses 1-based indexing for self.num (translating to 0-based list index).
        """
        obj_data = self._get_object_data()
        code: list[str] = obj_data.setdefault("code", [])
        
        target_index = self.num - 1
        
        # Ensure the code list is long enough before modifying
        while len(code) <= target_index:
            code.append("")
                    
        obj_data["changed"] = True
        obj_data["dirty"] = True
        code[target_index] = self.text.text
        self.highlight()

    def highlight(self):
        segments = self.highlighter.get_segments(self.text.text)
        self.text.set_segments(segments)

