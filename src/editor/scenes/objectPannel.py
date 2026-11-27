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

        self.creating = False
        self.create: NewObj = None

    def gen(self, _objs):
        for obj in self.objs:
            self.pan.remove_object(obj)
        self.objs.clear()
        y = 5
        for k, v in _objs.items():
            self.objs.append(self.pan.add_object(PanObj(y, k, v[0], self.pan, v[1])))
            y+=self.objs[-1].btn.dim.y+5
        self._objs = _objs

    def set_new_obj(self, name):
        if name in self._objs: return #name already used
        if len(self.objs)!=0: line = self.objs[-1].num
        else: line = self.find_place()
        Project.CHNG_NEWOBJ = {"check": True, "name": name, "line": line}

    def find_place(self) -> int:
        for line in getattr(Project, "scenes")[self.name]["code"]:
            line: str
            i = line.split("_")
            if len(i)>3:
                if line.split("_")[2] == "init": return Project.scenes[self.name]["code"].index(line)+2
            
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

        if self.creating and self.create: 
            self.create.update()
            if not self.create.input.btn.pressed:
                n = self.create.get()
                self.creating = False
                self.create = None
                self.set_new_obj(n)
        elif Keys.is_held(Keys.a) and Keys.is_pressed(Keys.a) and not self.creating:
            self.creating = True
            y = 5
            if len(self.objs)!=0: y+=self.objs[-1].btn.dim.y+self.objs[-1].btn.pos.y
            self.create = NewObj(y, self.pan)

    def render(self, screen):
        self.pan.render(render_sub=False)
        if self.creating and self.create: self.create.render(self.pan.screen)
        self.pan.sub.render()

class NewObj:
    def __init__(self, y, pan: Pannel):
        self.input = TextInput(btn(5, y, pan.dim.x-10, 50, [29, 34, 41], "", "white", 45, "white", -1, 2, True, sub=pan.sub))
        self.input.btn.pressed = True

    def get(self):
        return self.input.btn.text.text

    def update(self):
        self.input.update()

    def render(self, screen):
        self.input.render(screen)

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

