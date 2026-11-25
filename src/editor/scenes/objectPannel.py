import pygame

from PyScene import Vector2D

from ...Net import Net, _project
from ...utils import *
from .PropertiesPan import Properties

Project: _project = None

class ObjectsPannel:
    def __init__(self, w, pan: Pannel, project: _project, sceneName):
        global Project
        Project = project
        self.w = w
        self.P_pan = pan
        self.name = sceneName

        self.pan = Pannel(0, 0, w, pan.dim.y, (39, 41, 48), displaySurface=pan.screen, parent=pan.sub)

        self.objs: list[PanObj] = []

        self.prop: Properties = None
        self.last = None

    def gen(self, _objs):
        for obj in self.objs:
            self.pan.remove_object(obj)
        self.objs.clear()
        y = 5
        for k, v in _objs.items():
            self.objs.append(self.pan.add_object(PanObj(y, k, v[0], self.pan, v[1])))
            y+=self.objs[-1].btn.dim.y+5
            
    def update(self):
        i = False
        for obj in self.objs: 
            obj.update()
            if obj.btn.pressed:
                i = True
                if obj != self.last:
                    self.last = obj 
                    self.prop = self.pan.add_object(Properties(self.w, self.name, obj.name, obj._type, obj.num, self.P_pan, Project))
        if not i:
            self.pan.remove_object(self.prop)
            self.prop = None
        elif self.prop is not None: self.prop.update()


    def render(self, screen):
        self.pan.render()

class PanObj:
    def __init__(self, y, name, _type, pan: Pannel, num):
        r = pan.sub.get_global_rect(pygame.Rect(0, 0, pan.dim.x, pan.dim.y))
        self.btn = btn(5, y, pan.dim.x-10, 50, [29, 34, 41], f"{name}  |  ({_type})", "white", 45, "white", -1, 2, True, r, sub=pan.sub, toggleSelf=False)
        self.name = name
        self._type = _type
        self.num = num

    def update(self):
        self.btn.update()

    def render(self, screen):
        self.btn.render(screen)

