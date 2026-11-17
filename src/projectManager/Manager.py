import pygame
import sys
import os
from PyScene import Vector2D

from ..utils import *
from ..Net import Net

class ProjectManager:
    def __init__(self):
        #Net = Net.reset()

        #screen and basics
        Net.screen_size = Vector2D(1024, 600)
        Net.screen = pygame.display.set_mode(Net.screen_size.to_int())
        pygame.display.set_caption("AnotherEngine Project Manager")
        Net.screen_rect = Net.screen.get_rect()
        Net.clock = pygame.time.Clock()
        Net.dt = 0.0

        self.pan = Pannel(0, 0, Net.screen_size.x, 40, [29, 34, 41], displaySurface=Net.screen)
        self.pan.add_object(Text(35, "Project Manager", (255, 255, 255), Vector2D(5, 5), "topleft"))

        self.topBar = TopBar()
        self.projectList = ProjectList()

    def Run(self):
        while True:
            Net.update()
            self.update()
            self.render()

    def update(self):
        self.topBar.update()
        self.projectList.update()

    def render(self):
        Net.screen.fill([29, 34, 41])

        self.topBar.render()
        self.pan.render()
        self.projectList.render()

        Net.mouse_cursor()
        pygame.display.flip()

class TopBar:
    def __init__(self):
        self.pos = Vector2D(5, 40)
        self.pan = Pannel(self.pos.x, self.pos.y, Net.screen_size.x-10, 50, [54, 61, 74], "black", displaySurface=Net.screen)
        self.create = self.pan.add_object(btn(5, 5, 100, 40, [29, 34, 41], "+ Create", (255, 255, 255), 30, "white", -1, 2, sub=self.pan.sub))
        self.rescan = self.pan.add_object(btn(125, 5, 100, 40, [29, 34, 41], "rescan", (255, 255, 255), 30, "white", -1, 2, sub=self.pan.sub))
        self.importBtn = self.pan.add_object(btn(245, 5, 100, 40, [29, 34, 41], "import", (255, 255, 255), 30, "white", -1, 2, sub=self.pan.sub))

    def update(self):
        self.create.update()
        self.rescan.update()
        self.importBtn.update()

    def render(self):
        self.pan.render()

class ProjectList:
    def __init__(self):
        self.pos = Vector2D(10, 90)
        self.size = Vector2D(Net.screen_size.x-160, Net.screen_size.y-130)
        self.pannel = Pannel(self.pos.x, self.pos.y, self.size.x, self.size.y, [33, 38, 46], "black", displaySurface=Net.screen)

        self.projects: list[Project] = []

        self.gen()

    def gen(self):
        self.projects.clear()

        for folder in os.listdir(Net.save_dir):
            if folder.endswith(".engine"):
                y = 5 + len(self.projects) * 55
                self.projects.append(Project(y, folder, self.pannel.sub))

    def update(self):
        for project in self.projects:
            project.update()

    def render(self):
        self.pannel.render(render_sub=False)

        for project in self.projects:
            project.render()

        self.pannel.sub.render()

class Project:
    def __init__(self, y, folderName, sub): #folder name is NAME.engine
        self.pos = Vector2D(10, y)
        self.size = Vector2D(Net.screen_size.x-180, 50)
        self.Psub = sub
        self.pannel = Pannel(self.pos.x, self.pos.y, self.size.x, self.size.y, [54, 61, 74], "black", displaySurface=sub.screen, parent=sub)

        self.folderName = folderName
        self.name = folderName.split(".")[0]

        self.pannel.add_object(Text(35, self.name, (255, 255, 255), Vector2D(5, self.size.y//2), "midleft"))

    def update(self):
        pass

    def render(self):
        self.pannel.render()

