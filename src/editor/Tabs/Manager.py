import pygame

from PyScene import Vector2D

from ...Net import Net, _project
from ...utils import *

from .ManagerTab import ManagerTab
from ._tab import Tab

Project: _project = None

class TabManager:
    def __init__(self, project):
        global Project
        Project = project

        self.pannel = Pannel(0, 50, Net.screen_size.x, 60, [29, 34, 41], displaySurface=Net.screen)
        Net._y = self.pannel.pos.y+self.pannel.dim.y

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
        self.tabs.append(ManagerTab(self._y(), self.pannel.sub, r, Project))

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
        

