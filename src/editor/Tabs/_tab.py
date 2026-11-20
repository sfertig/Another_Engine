import pygame
from PyScene import Vector2D
from ...utils import *
from ...Net import _project

Project: _project = None

class Tab:
    def __init__(self, x: int, name: str, sub: SubScreen, rect: pygame.Rect, project, closebtn=True):
        global Project
        Project = project

        self.pos = Vector2D(x, 0)
        #find len of text
        font = 45
        n = f"{name}  x"
        self.w = Text(font, n, (0, 0, 0)).surface.get_width()+20
        #print(name, self.w, x)
        self.btn = btn(x, 0, self.w, sub.dim.y, [29, 34, 41], name, "white", font, "black", -1, 3, True, rect, sub, 10, False)
        self.active = False
        self._type_ = "none"
        self._name = name
        self._n = n
        self.close_rect = pygame.Rect(x+self.w-30, 20, 25, sub.dim.y-40)
        self.closebtn = btn(x+self.w-30, 20, 25, sub.dim.y-40, (0, 0, 0), minw=-1, maxw=2, sub=sub)
        self.clsbtn = closebtn
        self._sub = sub

    def set_x(self, x):
        self.pos.x = x
        self.btn.set_x(x)
        self.closebtn.set_x(x+self.w-30)
        self.close_rect = pygame.Rect(x+self.w-30, 20, 25, self._sub.dim.y-40)

    def on_active(self): 
        if self.clsbtn: self.btn.text.set_text(self._n)
        self.active = True
    def on_passive(self): 
        if self.clsbtn: self.btn.text.set_text(self._name)
        self.active = False
    def on_close(self): pass
    def on_open(self): pass

    #methods used by children
    def _update(self): pass
    def _render(self): pass
    def _close(self): 
        print(self.active)
        Project.CLS_TB["check"] = True
        Project.CLS_TB["name"] = self._name
        Project.CLS_TB["type"] = self._type_


    def update(self):
        if self.clsbtn and self.active: 
            if self.closebtn.update() or (Keys.is_held(Keys.control) and Keys.is_pressed(Keys.w)): self._close()

        if self.btn.update():
            if not self.active: 
                self.on_active()
                self.active = True
        elif self.active:
            self.on_passive()
            self.active = False
        if self.active: self._update()

    def render(self, screen):
        self.btn.render(screen)
        if self.active and self.clsbtn: 
            pygame.draw.rect(screen, "white", self.close_rect, self.closebtn.w)
        if self.active: self._render()