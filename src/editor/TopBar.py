import pygame

from PyScene import Vector2D

from ..Net import Net, _project
from ..utils import *

from ..build.Build import BuildProject
from ..runner.Run import Runner

Project: _project = None

class TopBar:
    def __init__(self, project: _project):
        global Project
        Project = project

        self.pan = Pannel(0, 0, Net.screen_size.x, 50, [29, 34, 41], displaySurface=Net.screen)
        self.run = self.pan.add_object(btn(Net.screen_size.x-300, 2, 120, 46, [29, 34, 41], "Run (f5)", (255, 255, 255), 40, "white", -1, 2, sub=self.pan.sub))
        self.build = self.pan.add_object(btn(Net.screen_size.x-140, 2, 120, 46, [29, 34, 41], "Build (f6)", (255, 255, 255), 40, "white", -1, 2, sub=self.pan.sub))

    def update(self):
        if self.run.update():
            BuildProject(Project.folder).gen()
            Runner(Project.folder)
        if self.build.update():
            BuildProject(Project.folder).gen()

    def render(self):
        self.pan.render()
