import pygame

from PyScene import Vector2D

from ...Net import Net, _project
from ...utils import *

Project: _project = None

class TabManager:
    def __init__(self, project):
        global Project
        Project = project

        self.pannel = Pannel(0, 50, Net.screen_size.x, 40, [29, 34, 41], displaySurface=Net.screen)

        self.tabs: list[Tab] = []
        self.gen()

    def _y(self):
        return self.tabs[-1].btn.rect.width + 5

    def gen(self):
        self.tabs.clear()
        #default tabs
        r = pygame.Rect(0, 0, Net.screen_size.x, self.pannel.dim.y)
        self.tabs.append(Tab(10, "Settings", self.pannel.sub, r))
        self.tabs.append(Tab(self._y(), "Assets", self.pannel.sub, r))
        self.tabs.append(Tab(self._y(), "Tabs", self.pannel.sub, r))

        for tab in self.tabs:
            self.pannel.add_object(tab)

    def update(self):
        for tab in self.tabs:
            tab.update()

    def render(self):
        self.pannel.render()
        


class Tab:
    def __init__(self, x: int, name: str, sub: SubScreen, rect: pygame.Rect):
        self.pos = Vector2D(x, 0)
        #find len of text
        w = Text(30, name, (0, 0, 0)).surface.get_width()
        self.btn = btn(x, 0, w+10, 40, [29, 34, 41], name, "white", 30, "black", -1, 2, True, rect, sub)

    def update(self):
        self.btn.update()

    def render(self, screen):
        self.btn.render(screen)


