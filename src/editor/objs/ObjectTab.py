import pygame
import os

from ...Net import Net, _project
from ...utils import *
from ..Tabs._tab import Tab

from .CodePannel import CodePannel

Project: _project = None

class ObjTab(Tab):
    def __init__(self, x, sub, name, rect, project: _project):
        global Project
        Project = project

        super().__init__(x, name, sub, rect, Project, True)
        self._type_ = "object"

        self.pan = Pannel(0, Net._y, Net.screen_size.x, Net.screen_size.y-Net._y, [29, 34, 41], displaySurface=Net.screen)
        self.pan.add_object(Line(20, 2, self.pan.dim.x-20, 2))

        self.code = self.pan.add_object(CodePannel(10, 0, Net.screen_size.x-500, Net.screen_size.y-Net._y, name, "object", project, self.pan))

    def _update(self):
        self.code.update()

    def _render(self):
        self.pan.render()
