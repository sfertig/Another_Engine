import pygame
import os
import importlib.util
import importlib
from pathlib import Path
import sys
import ast

from PyScene import Vector2D

from ...Net import Net, _project
from ...utils import *

import PyScene as py 
from PyScene import *


Project: _project = None

class VisualPannel:
    def __init__(self, x, y, w, h, objs, pan: Pannel, project, name):
        global Project
        Project = project

        self.zoom = 4.0
        self.display = SubScreen(x, y, w, h, "black", pan.screen, pan.sub) # <- sub that displays to ui
        dw, dh = self.display.screen.get_size()
        self.screen = pygame.Surface((int(dw / self.zoom), int(dh / self.zoom)))
        self.cam = Vector2D(0, 0)
        #test objs
        py.Game.init(w, h, "none", _no_dir=True, _screenCam=False)
        self._objs: dict = objs
        self.name = name
        self.objs: list[py.GameObj] = []
        self.grid = Grid(16)

        #mouse stuff
        self.click_pos = Vector2D(0, 0)
        self.down = False
        self.minZoom = 1.0
        self.maxZoom = 8.0
        self.DefaultZoom = self.zoom

        #self.gen()

    def gen(self):
        #print(self._objs)
        for obj in self.objs:
            try: obj.destroy()
            except: pass
        self.objs.clear()
        builds = os.listdir(Project.path+"_buildcache_/")
        for k, v in self._objs.items():
            line: str = Project.scenes[self.name]["code"][v[1]-1]
            #print(line, v)
            #determine if file is built
            name, _type = k, v[0]
            if _type+".py" not in builds and not hasattr(py, _type):
                print(f"[VisualScenePannel] - NOTICE: no build file found for {name} ({_type})")
                continue
            if "=" not in line: continue

            construct = line.split("=", 1)[1].strip()
            if hasattr(py, _type):
                obj = run_construct(getattr(py, _type), construct)
            else:                
                cls = import_class_from_path(Project.path+"_buildcache_/"+_type+".py", _type)
                obj = run_construct(cls, construct)
            if obj is not None: self.objs.append(obj)
            

    def handle_dragging(self):
        if Keys.is_pressed(Keys.f):
            self.cam = Vector2D(0, 0)
            self.down = False
            self.zoom = self.DefaultZoom
            dw, dh = self.display.screen.get_size()
            self.screen = pygame.Surface((int(dw / self.zoom), int(dh / self.zoom)))
            return
        mouse_down = pygame.mouse.get_pressed()[0]
        curr_pos = self.display.local_mouse_pos()
        if self.down and not mouse_down:
            self.down = False
            return  # mouse is up
        elif self.down and mouse_down:
            # Divide by 2 to match self.screen's half-resolution scale
            delta_x = (curr_pos.x - self.click_pos.x) / self.zoom
            delta_y = (curr_pos.y - self.click_pos.y) / self.zoom
            self.cam.x -= delta_x
            self.cam.y -= delta_y
            self.click_pos = curr_pos
        elif not self.down and mouse_down:
            # Only start dragging if the click began inside this panel
            w, h = self.display.screen.get_size()
            if 0 <= curr_pos.x <= w and 0 <= curr_pos.y <= h:
                self.down = True
                self.click_pos = curr_pos

    def handle_zoom(self):
        if Net.scroll != 0.0:
            self.zoom = clamp(self.zoom-Net.scroll/10, self.minZoom, self.maxZoom)
            dw, dh = self.display.screen.get_size()
            self.screen = pygame.Surface((int(dw / self.zoom), int(dh / self.zoom)))

    def update(self):
        self.handle_dragging()
        self.handle_zoom()

    def render(self, screen):
        #self.display.clear()
        self.screen.fill("black")
        self.grid.render(self.screen, self.cam)
        for obj in self.objs:
            if obj is not None: obj.render(self.screen, self.cam)
        self.display.screen.blit(pygame.transform.scale(self.screen, self.display.dim.to_int()))
        self.display.render()

class Grid:
    def __init__(self, size: int = 16):
        self.size = size

    def render(self, screen, cam: Vector2D):
        w, h = screen.get_size()
        color = (50, 50, 50)

        # Calculate the screen-space offset for the first visible lines
        offset_x = -(cam.x % self.size)
        offset_y = -(cam.y % self.size)

        # Vertical lines
        for x in range(int(offset_x), w, self.size):
            pygame.draw.line(screen, color, (x, 0), (x, h))

        # Horizontal lines
        for y in range(int(offset_y), h, self.size):
            pygame.draw.line(screen, color, (0, y), (w, y))

def import_class_from_path(file_path: str, class_name: str):
    # 1. Create a unique module name from the file stem
    module_name = Path(file_path).stem
    
    # 2. Load the module specification and create the module object
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {file_path}")
        
    module = importlib.util.module_from_spec(spec)
    
    # 3. Register in sys.modules (helps if the module uses relative imports)
    sys.modules[module_name] = module
    
    # 4. Execute the module to populate its attributes
    spec.loader.exec_module(module)
    
    # 5. Retrieve and return the class from the module
    return getattr(module, class_name)

import ast

def run_construct(imported_cls, construct_str: str):
    # Extracts "player" from 'player(100, 100, "green")'
    call_name = construct_str.split("(", 1)[0].strip()    
    # Maps that exact name to your imported class and executes it
    try:
        return eval(construct_str, {"__builtins__": {}}, {call_name: imported_cls})
    except:
        print("[ERROR] - NOTICE: an error was caught when creating an object, object will not be shown")
        return None




