import pygame
import os
import sys
from PyScene import Vector2D
import json


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

    def load(self):
        with open(self.path+"_project.json", "r") as f:
            self.project = json.load(f)
        #later load scenes and objs

    def save(self):
        self._saveFile(self.project, self.path+"_project.json")

    def _saveFile(self, data, path):
        if data["changed"]:
            data["changed"] = False
            name = path.split("/")[-2].split(".")[0]
            print(f"Saved {name}")
            with open(path, "w") as f:
                json.dump(data, f, indent=4)

