import pygame
import os

from ...Net import Net, _project
from ...utils import *
from ..Tabs._tab import Tab
from ...build.Build import BuildProject

from ..objs.CodePannel import CodePannel
from .TopBar import SceneTopBar
from .VisualScene import VisualSceneEditor

Project: _project = None

class SceneTab(Tab):
    def __init__(self, x, sub, name, rect, project: _project):
        global Project
        Project = project

        super().__init__(x, name, sub, rect, Project, True)
        self._type_ = "scene"

        self.pan = Pannel(0, Net._y, Net.screen_size.x, Net.screen_size.y-Net._y, [29, 34, 41], displaySurface=Net.screen)
        self.pan.add_object(Line(20, 2, self.pan.dim.x-20, 2))
        self.bar = self.pan.add_object(SceneTopBar(self.pan))

        self.code = CodePannel(0, 10+self.bar.height, Net.screen_size.x, self.pan.dim.y-10-self.bar.height, name, "scene", project, self.pan)
        self.vis = VisualSceneEditor(name, 10+self.bar.height, self.pan, Project, self.code)
        self.mode = "visual"

        #debug
        #self.bar.toggle.pressed = True

    def set_mode(self):
        #keybinds
        last = self.mode
        if Keys.is_pressed(Keys.f2): self.bar.toggle.pressed = not self.bar.toggle.pressed
        if self.bar.toggle.pressed: 
            self.mode = "coding"
            if last == "visual": self.code.gen()
        else: 
            self.mode = "visual"
            if last == "coding": 
                Project.save()
                BuildProject(Project.folder).gen()
                Project._save_dirty()
                self.vis.gen()
        #handle reload
        if Keys.is_held(Keys.control) and Keys.is_pressed(Keys.r): self.vis.gen()

    def _update(self):
        self.set_mode()
        self.bar.update()

        if self.mode == "coding": self.code.update()
        else: self.vis.update()

    def _render(self):
        self.pan.render(render_sub=False)
        if self.mode == "coding": self.code.render(None)
        else: self.vis.render()
        self.pan.sub.render()
