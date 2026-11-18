import pygame
import os
import sys
from PyScene import Vector2D
import json

from .utils import DEFAULTPROJECT


class _Net:
    def __init__(self):
        self.screen: pygame.Surface = None
        self.screen_rect: pygame.Rect = None
        self.screen_size: Vector2D = None
        self.clock: pygame.time.Clock = None
        self.dt: float = None
        self.events = None

        self.mouse_down = False
        self.click = False
        self._y = 0
        self.scroll = 0

        #file stuff
        self.save_dir: str = None

        self.cursor = pygame.SYSTEM_CURSOR_ARROW
        self._last_cursor = None

        self.VERSION = "0.0.1"

        self.manager = None # <- to return to manager after editor

    def reset(self):
        pygame.quit()
        pygame.init()

    def update(self, esc=True):
        self.scroll = 0
        _esc = False
        self.cursor = pygame.SYSTEM_CURSOR_ARROW
        self.click = False
        self.events = pygame.event.get()
        self.dt = self.clock.tick(60) / 1000.0
        for event in self.events:
            if event.type == pygame.QUIT:
                if esc: sys.exit()
                else: _esc = True
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1: 
                    self.mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP and self.mouse_down: 
                if event.button == 1: 
                    self.mouse_down = False
                    self.click = True
            elif event.type == pygame.MOUSEWHEEL: self.scroll = -event.y
        return _esc

    def mouse_cursor(self):
        if self.cursor != self._last_cursor:
            pygame.mouse.set_cursor(self.cursor)
            self._last_cursor = self.cursor

    def folder_name(self, name):
        _text = name
        #make the text folder safe
        for char in ["\\", "/", ":", "*", "?", "\"", "<", ">", "|", ".", " ", "#", "%", "$", "&", "@", "!", "^"]:
            _text = _text.replace(char, "_")
        _text += ".engine"
        return _text


Net: _Net = _Net()

#editor stuff

class _project:
    def __init__(self, name: str):
        self.name = name
        self.folder = name+".engine"
        self.path = f"{Net.save_dir}/{self.folder}/"

        #load json data
        self.load()
        self._updateProject()

        #reload flags
        self.RLD_MANAGER = False #reloads managerTab fo new / del files

    def load(self):
        with open(self.path+"_project.json", "r") as f:
            self.project = json.load(f)
        #load scenes
        self.scenes = {}
        for scene in os.listdir(self.path+"scenes/"):
            with open(self.path+"scenes/"+scene, "r") as f:
                self.scenes[scene.split(".")[0]] = json.load(f)

        #objs
        self.objects = {}
        for obj in os.listdir(self.path+"objects/"):
            with open(self.path+"objects/"+obj, "r") as f:
                self.objects[obj.split(".")[0]] = json.load(f)

    def save(self):
        self._saveFile(self.project, self.path+"_project.json")
        
        """for scene, data in self.scenes.items():
            self._saveFile(data, self.path+"scenes/"+scene+".json") 

        for obj, data in self.objects.items():
            self._saveFile(data, self.path+"objects/"+obj+".json")"""

    def _saveFile(self, data, path):
        if data["changed"]:
            data["changed"] = False
            name = path.split("/")[-2].split(".")[0]
            print(f"Saved {name}")
            with open(path, "w") as f:
                json.dump(data, f, indent=4)

    def _updateProject(self): #updates files with new keys
        #if self.project["version"] == Net.VERSION: return

        #ensure all folders exist
        for folder in ["_buildcache_", "objects", "scenes", "assets"]:
            if folder not in os.listdir(self.path):
                os.mkdir(self.path+folder)

        # start updating
        self.project = self._update_file(self.project, DEFAULTPROJECT)

    def _update_file(self, data, newdata) -> dict:
        for key, value in newdata.items():
            # Check if the key exists in data and BOTH values are dictionaries
            if (
                key in data
                and isinstance(data[key], dict)
                and isinstance(value, dict)
            ):
                # Recursively update the nested dictionary
                self._update_file(data[key], value)
            else:
                # Otherwise, add the new key or overwrite the existing non-dict value
                data[key] = value

        return data



