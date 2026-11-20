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
        self.pan.add_object(Line(20, 47, Net.screen_size.x-20, 47))

    def update(self):

        if self.run.update() or Keys.is_pressed(Keys.f5):
            Project.save()
            BuildProject(Project.folder).gen()
            Project._save_dirty()
            Runner(Project.folder)
        if self.build.update() or Keys.is_pressed(Keys.f6):
            Project.save()
            BuildProject(Project.folder).gen()
            Project._save_dirty()

        if Keys.is_pressed(Keys.f1) or (Keys.is_held(Keys.control) and Keys.is_pressed(Keys.s)): Project.save()

    def render(self):
        self.pan.render()
