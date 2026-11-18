import pygame
from PyScene import Vector2D
from ...utils.ui import btn, Text, SubScreen

class Tab:
    def __init__(self, x: int, name: str, sub: SubScreen, rect: pygame.Rect):
        self.pos = Vector2D(x, 0)
        #find len of text
        font = 45
        self.w = Text(font, name, (0, 0, 0)).surface.get_width()+10
        #print(name, self.w, x)
        self.btn = btn(x, 0, self.w, sub.dim.y, [29, 34, 41], name, "white", font, "black", -1, 3, True, rect, sub, 10, False)
        self.active = False

    def on_active(self): pass
    def on_passive(self): pass
    def on_close(self): pass
    def on_open(self): pass

    def _update(self): pass
    def _render(self): pass


    def update(self):
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
        if self.active: self._render()