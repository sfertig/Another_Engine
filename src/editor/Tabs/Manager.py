import pygame

from PyScene import Vector2D

from ...Net import Net, _project
from ...utils import *

Project: _project = None

class TabManager:
    def __init__(self, project):
        global Project
        Project = project

        self.pannel = Pannel(0, 50, Net.screen_size.x, 60, [29, 34, 41], displaySurface=Net.screen)

        self.tabs: list[Tab] = []
        self.gen()

    def _y(self):
        return self.tabs[-1].pos.x + self.tabs[-1].btn.rect.width + 20

    def gen(self):
        self.tabs.clear()
        self.lastActive = 2
        #default tabs
        r = pygame.Rect(0, self.pannel.pos.y, Net.screen_size.x, self.pannel.dim.y)
        self.tabs.append(Tab(10, "Settings", self.pannel.sub, r))
        self.tabs.append(Tab(self._y(), "Assets", self.pannel.sub, r))
        self.tabs.append(Tab(self._y(), "Tabs", self.pannel.sub, r))

        self._activate(self.lastActive)

        for tab in self.tabs:
            self.pannel.add_object(tab)

    def _activate(self, index):
        self.tabs[index].btn.pressed = True
        self.tabs[self.lastActive].active = True
        self.tabs[self.lastActive].on_active()


    def update(self):
        active = False
        for tab in self.tabs:
            tab.update()
            if tab.btn.pressed: 
                active = True
                self.lastActive = self.tabs.index(tab)
        if not active: self._activate(self.lastActive)

    def render(self):
        self.pannel.render()
        


class Tab:
    def __init__(self, x: int, name: str, sub: SubScreen, rect: pygame.Rect):
        self.pos = Vector2D(x, 0)
        #find len of text
        font = 45
        self.w = Text(font, name, (0, 0, 0)).surface.get_width()+10
        #print(name, self.w, x)
        self.btn = btn(x, 0, self.w, sub.dim.y, [29, 34, 41], name, "white", font, "black", -1, 3, True, rect, sub, 10, False)
        self.active = False

    def on_active(self): print("active")
    def on_passive(self): print("passive")
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


