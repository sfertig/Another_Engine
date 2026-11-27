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
        self.args: list[InputSlice] = []
        y = 5
        for name, v in match.items():
            self.args.append(self.pan.add_object(InputSlice(y, name, v[0], v[1], self.pan)))
            y += self.args[-1].sub.dim.y+5
        self.match = match

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
            code_content = "\n".join(Project.objects[self._type].get("code", []))
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

    def set_line(self):
        line = f"        self.{self.obj} = {self._type}("
        for arg in self.args:
            line += str(arg.get_value())+", "
        if len(self.args)>0: line = line[:-2]
        line += ")"
        Project.scenes[self.name]["code"][self.num] = line
        Project.scenes[self.name]["dirty"] = True
        Project.scenes[self.name]["changed"] = True

    def update(self):
        for arg in self.args:
            arg.update()
        #test / debug
        for i in self.args:
            if i.get_value() != self.match[i._name][0]:
                self.set_line()
                Project.RLD_VIS = True
                break

    def render(self, screen):
        self.pan.render()

class InputSlice:
    def __init__(self, y, name, value, _type, pan: Pannel):
        self.sub = SubScreen(5, y, pan.dim.x-10, 50, [29, 34, 41], pan.screen, pan.sub)
        self.screen = self.sub.screen
        self.name = Text(45, name+":", "white", Vector2D(3, 25), "midleft")
        self._name = name
        if _type in Types:
            self.value = Types[_type](self.sub, _type, value)
        else: self.value = Undefined(self.sub, _type, value)
        self.default = value
        
    def get_value(self):
        if type(self.value) != Undefined: 
            return self.value.get_value()
        else: return self.default

    def update(self):
        self.value.update()

    def render(self, screen):
        self.sub.clear()
        self.name.render(self.screen)
        self.value.render()
        self.sub.render()


#region Inputs
class Input:
    def __init__(self, sub, _type, value):
        w = sub.dim.x//1.5-5
        self.sub = SubScreen(sub.dim.x-w, 2, w, sub.dim.y-4, "black", sub.screen, sub)
        self.height = self.sub.dim.y
        self.screen = self.sub.screen
        self.value = value
        self._type = _type
    def get_value(self): pass
    def update(self): pass
    def render(self): pass

class IntInput(Input): 
    def __init__(self, sub, _type, value):
        super().__init__(sub, _type, value)
        self.input = TextInput(btn(0, 0, self.sub.dim.x, self.sub.dim.y, "black", str(value), "white", self.height-5, "white", -1, 2, True, sub=self.sub))

    def get_value(self): return int(self.input.btn.text.text)

    def update(self):
        self.input.update()
        self.input.btn.text.set_text(format_int(self.input.btn.text.text))

    def render(self):
        self.sub.clear()
        self.input.render(self.screen)
        self.sub.render()

class vector2dInput(Input):
    def __init__(self, sub, _type, value):
        super().__init__(sub, _type, value)
        self.x = TextInput(btn(0, 0, self.sub.dim.x//2-5, self.sub.dim.y, "black", str(value[0]), "white", self.height-5, "white", -1, 2, True, sub=self.sub))
        self.y = TextInput(btn(self.sub.dim.x//2+5, 0, self.sub.dim.x//2-5, self.sub.dim.y, "black", str(value[1]), "white", self.height-5, "white", -1, 2, True, sub=self.sub))
        self.sub.color = [29, 34, 41]

    def update(self):
        self.x.update()
        self.y.update()
        self.x.btn.text.set_text(format_int(self.x.btn.text.text))
        self.y.btn.text.set_text(format_int(self.y.btn.text.text))

    def render(self):
        self.sub.clear()
        self.x.render(self.screen)
        self.y.render(self.screen)
        self.sub.render()

class Undefined(Input):
    def __init__(self, sub, _type, value):
        super().__init__(sub, _type, value)
        self.text = Text(self.height-5, "undefined", "white", Vector2D(self.sub.dim.x//2, self.sub.dim.y//2))

    def render(self):
        self.sub.clear()
        self.text.render(self.screen)
        self.sub.render()


Types: dict[str, any] = {
    "int": IntInput,
    "Vector2D": vector2dInput,

}

#region formats
def format_int(text: str) -> str:
    digits = "".join(char for char in text if char.isdigit() or char=="-")
    return digits.lstrip("0") or "0"

