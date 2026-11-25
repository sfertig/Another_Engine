import pygame

from PyScene import Vector2D
import ast
import inspect

import PyScene as py

from ...Net import Net, _project
from ...utils import *

Project: _project = None

class Properties:
    def __init__(self, w, sceneName, objName, _type, lineNum, pan: Pannel, project: _project):
        global Project
        Project = project

        self.pan = Pannel(pan.dim.x-w, 0, w, pan.dim.y, (39, 41, 48), displaySurface=pan.screen, parent=pan.sub)
        self.name = sceneName
        self.obj = objName
        self._type = _type
        self.num = lineNum-1

        self.line: str = Project.scenes[sceneName]["code"][lineNum-1].strip()
        #print(self.line)
        self.get_inputs()

    def get_inputs(self):
        custom = not hasattr(py, self._type)
        #get values
        construct = self.line.split("=")[1].strip()
        construct = construct.split("(")[1].replace(")", "")
        values = []
        for i in construct.split(","):
            values.append(i.strip())
        #get arg names
        names = []
        func = ""
        if custom: #custom obj, easy method!
            for line in Project.objects[self.obj]["code"]:
                line: str
                i = line.split("_")
                if len(i)>3:
                    if line.split("_")[2] == "init":
                        func = line.strip().split("(")[-1].replace(")", "").replace(":", "").strip()
                        break
            for arg in func.split(","):
                if arg.strip() != "self": names.append(arg.strip())
        else: #pyscene obj, harder method
            obj = getattr(py, self._type)
            sig = inspect.signature(obj.__init__)
            names = [name for name in sig.parameters if name != "self"]

        #match names and values
        match = dict(zip(names, values))
        print(match)
            



    def update(self):
        pass

    def render(self, screen):
        self.pan.render()
