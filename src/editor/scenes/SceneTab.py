import pygame
import os

from ...Net import Net, _project
from ...utils import *
from ..Tabs._tab import Tab

from ..objs.CodePannel import CodePannel
from .TopBar import SceneTopBar

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
        self.mode = "visual"

    def set_mode(self):
        #keybinds
        if Keys.is_pressed(Keys.f2): self.bar.toggle.pressed = not self.bar.toggle.pressed
        if self.bar.toggle.pressed: self.mode = "coding"
        else: self.mode = "visual"

    def _update(self):
        self.set_mode()
        self.bar.update()

        if self.mode == "coding": self.code.update()

    def _render(self):
        self.pan.render(render_sub=False)
        if self.mode == "coding": self.code.render(None)
        self.pan.sub.render()
