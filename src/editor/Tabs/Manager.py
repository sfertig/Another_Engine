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
        self.r = pygame.Rect(0, self.pannel.pos.y, Net.screen_size.x, self.pannel.dim.y)

        self.tabs: list[Tab] = []
        self.gen()

    def _y(self):
        return self.tabs[-1].pos.x + self.tabs[-1].btn.rect.width + 20

    def gen(self):
        self.tabs.clear()
        self.lastActive = 2
        #default tabs
        r = self.r
        self.tabs.append(Tab(10, "Settings", self.pannel.sub, r, Project, False))
        self.tabs.append(Tab(self._y(), "Assets", self.pannel.sub, r, Project, False))
        self.tabs.append(ManagerTab(self._y(), self.pannel.sub, r, Project))
        self.pannel.add_object(Line(self._y()-10, 2, self._y()-10, self.pannel.dim.y-2))

        self._activate(self.lastActive)

        for tab in self.tabs:
            self.pannel.add_object(tab)

    def _deactivate(self, index):
        self.tabs[index].btn.pressed = False
        self.tabs[index].active = False
        self.tabs[index].on_passive()

    def _activate(self, index):
        self.tabs[index].btn.pressed = True
        self.tabs[index].active = True
        self.tabs[index].on_active()
        self.lastActive = index

    def _shift(self, startindex=3): # <- shifts tabs left when one is closed
        for i in range(startindex, len(self.tabs)):
            btn = self.tabs[i]
            btn.set_x(self.tabs[i-1].pos.x+self.tabs[i-1].w+20)
            

    def open(self, name, _type_):
        #check if tab already open
        for tab in self.tabs:
            if tab._name == name:
                self._deactivate(self.lastActive)
                self._activate(self.tabs.index(tab))
                return

        print("[TabManager] - New "+_type_+" tab opened: "+name)
        self._deactivate(self.lastActive)
        self.tabs.append(self.pannel.add_object(Tab(self._y(), name, self.pannel.sub, self.r, Project)))
        self._activate(len(self.tabs)-1)

    def close(self, name, _type_):
        #check if tab already open
        for tab in self.tabs:
            if tab._type_ == _type_ and tab._name == name:
                index = self.tabs.index(tab)
                self.pannel.remove_object(tab)
                self.tabs.remove(tab)
                #activate tab to left
                self._activate(index-1)
                self._shift(index)

                print("[TabManager] - Closed Tab "+name)
                return

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
        

