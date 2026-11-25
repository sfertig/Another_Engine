import pygame
import os

from PyScene import Vector2D

from ...Net import Net, _project
from ...utils import *

from .VisualPannel import VisualPannel
from .objectPannel import ObjectsPannel
import PyScene as py 


Project: _project = None

class VisualSceneEditor:
    def __init__(self, name, y, pan: Pannel, project: _project, code):
        global Project
        Project = project

        self.pan = Pannel(0,  y, pan.dim.x, pan.dim.y-y, [29, 34, 41], displaySurface=pan.sub.screen, parent=pan.sub)
        self.code = code # <- may be used for objs in scene
        self.name = name
        i = 400
        self.objs = self.pan.add_object(ObjectsPannel(i-10, self.pan, Project, name))
        self.vis = self.pan.add_object(VisualPannel(i, 0, self.pan.dim.x-i*2, self.pan.dim.y, {}, self.pan, Project, name))
        self.gen()

    def gen(self):
        objs: dict[str, list] = {} #name, list[type, line num]
        start = False
        #search and define objects
        for line in getattr(Project, "scenes")[self.name]["code"]:
            line: str
            if not start: #searching for init func
                i = line.split("_")
                if len(i)>3:
                    if line.split("_")[2] == "init": start = True
            else:
                #check if should exit (if this is not a function)
                if "def" in line.split(" "): break
                #ignore super
                elif "super()" in line.split(".")[0].split(" "): continue
                #check for assignment
                elif "=" not in line: continue
                #chech that starts with self
                elif "self" not in line: continue
                elif line.strip()[0] == "#": continue
                #now its a self.__ = __, so get name and type
                name: str = line.split("=")[0].split(".")[1].replace(" ", "")
                _type: str = line.split("=")[1]
                if "(" not in _type: continue #dosnt create / define a GameObj
                _type = _type.split("(")[0].replace(" ", "")
                #check if type is a user created object (and later pyscene objects)
                if _type not in Project.objects and not hasattr(py, _type): continue

                objs[name] = [_type, getattr(Project, "scenes")[self.name]["code"].index(line)+1]
        #create objs
        self._objs = objs
        self.vis._objs = objs
        self.vis.gen()
        self.objs.gen(objs)

    def update(self):
        self.vis.update()
        self.objs.update()

    def render(self):
        self.pan.render()

