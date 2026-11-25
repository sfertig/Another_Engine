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
        match = self.get_inputs()
        print(match)

    def get_inputs(self):
        custom = not hasattr(py, self._type)
        
        # 1. Extract values from the constructor call string (e.g., player(16, 16, 32, 32, "yellow"))
        construct = self.line.split("=")[1].strip() if "=" in self.line else self.line
        try:
            construct = construct.split("(")[1].replace(")", "")
            values = [i.strip() for i in construct.split(",") if i.strip()]
        except IndexError:
            values = []

        names = []
        types = {}

        if custom:
            # Custom object: parse __init__ signature via AST from stored code lines
            code_content = "\n".join(Project.objects[self.obj].get("code", []))
            try:
                tree = ast.parse(code_content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name == "__init__":
                        for arg in node.args.args:
                            arg_name = arg.arg
                            if arg_name == "self":
                                continue
                            names.append(arg_name)
                            
                            if arg.annotation:
                                try:
                                    types[arg_name] = ast.unparse(arg.annotation)
                                except Exception:
                                    types[arg_name] = "undefined"
                            else:
                                types[arg_name] = "undefined"
                        break
            except SyntaxError:
                pass
                
        else:
            # PyScene object: use inspect module on compiled class
            obj = getattr(py, self._type)
            sig = inspect.signature(obj.__init__)
            for name, param in sig.parameters.items():
                if name == "self":
                    continue
                names.append(name)
                
                if param.annotation != inspect.Parameter.empty:
                    ann = param.annotation
                    if hasattr(ann, "__name__"):
                        types[name] = ann.__name__
                    else:
                        types[name] = str(ann)
                else:
                    types[name] = "undefined"

        # 2. Only map names that have a corresponding value defined in the construct string
        match = {}
        for idx, name in enumerate(names):
            if idx < len(values) and values[idx]:  # Checks that the value exists and isn't empty
                val = values[idx]
                t_str = types.get(name, "undefined")
                match[name] = [val, t_str]

        return match
            
    def update(self):
        pass

    def render(self, screen):
        self.pan.render()
