import pygame
import sys
import os
import shutil
import json
from PyScene import Vector2D
import copy

from ..utils import *
from ..Net import Net
from ..build.Build import BuildProject
from ..runner.Run import Runner
from ..editor.Run import RunEditor

RELOAD = False

class ProjectManager:
    def __init__(self):
        Net.reset()
        Net.manager = self.__class__
        #screen and basics
        Net.screen_size = Vector2D(1024, 600)
        Net.screen = pygame.display.set_mode(Net.screen_size.to_int())
        pygame.display.set_caption("AnotherEngine Project Manager")
        Net.screen_rect = Net.screen.get_rect()
        Net.clock = pygame.time.Clock()
        Net.dt = 0.0

        self.pan = Pannel(0, 0, Net.screen_size.x, 40, [29, 34, 41], displaySurface=Net.screen)
        self.pan.add_object(Text(35, "Project Manager", (255, 255, 255), Vector2D(5, 5), "topleft"))

        self.topBar = TopBar()
        self.projectList = ProjectList()

    def Run(self):
        while True:
            Net.update()
            self.update()
            self.render()

    def update(self):        
        self.topBar.update()
        self.projectList.update()

    def render(self):
        Net.screen.fill([29, 34, 41])

        self.topBar.render()
        self.pan.render()
        self.projectList.render()

        Net.mouse_cursor()
        pygame.display.flip()

class TopBar:
    def __init__(self):
        self.pos = Vector2D(5, 40)
        self.pan = Pannel(self.pos.x, self.pos.y, Net.screen_size.x-10, 50, [54, 61, 74], "black", displaySurface=Net.screen)
        self.create = self.pan.add_object(btn(Net.screen_size.x-120, 5, 100, 40, [29, 34, 41], "+ Create", (255, 255, 255), 30, "white", -1, 2, sub=self.pan.sub))
        self.rescan = self.pan.add_object(btn(10, 5, 100, 40, [29, 34, 41], "Rescan", (255, 255, 255), 30, "white", -1, 2, sub=self.pan.sub))
        self.importBtn = self.pan.add_object(btn(125, 5, 100, 40, [29, 34, 41], "Import", (255, 255, 255), 30, "white", -1, 2, sub=self.pan.sub))
        self.name = self.pan.add_object(TextInput(btn(Net.screen_size.x-310, 5, 180, 40, 
                                        [29, 34, 41], "", (255, 255, 255), 30, "white", -1, 2, True, sub=self.pan.sub)))

    def update(self):
        self.name.update()
        if self.create.update(): self._create()
        self.rescan.update()
        self.importBtn.update()

    def render(self):
        
        self.pan.render()

    def _create(self):
        global RELOAD
        name = Net.folder_name(self.name.btn.text.text)
        if name not in os.listdir(Net.save_dir):
            os.mkdir(os.path.join(Net.save_dir, name))
            p = os.path.join(Net.save_dir, name)+"/"
            RELOAD=True
            #populate folders and files
            os.mkdir(p+"assets")
            os.mkdir(p+"objects")
            os.mkdir(p+"scenes")
            os.mkdir(p+"_buildcache_")
            #make engine file
            n = name.split(".")[0]
            data = copy.deepcopy(DEFAULTPROJECT)
            data["project_name"] = n
            data["version"] = Net.VERSION
            data["window"]["title"] = n
            with open(p+"_project.json", "w") as f:
                json.dump(data, f, indent=4)
            with open(p+"build.py", "w") as f:
                f.write("")


class ProjectList:
    def __init__(self):
        self.pos = Vector2D(10, 90)
        self.size = Vector2D(Net.screen_size.x-160, Net.screen_size.y-130)
        self.pannel = Pannel(self.pos.x, self.pos.y, self.size.x, self.size.y, [33, 38, 46], "black", displaySurface=Net.screen)

        self.projects: list[Project] = []
        self.gen()

    def gen(self):
        self.projects.clear()
        for folder in os.listdir(Net.save_dir):
            if folder.endswith(".engine"):
                y = 5 + len(self.projects) * 55
                self.projects.append(Project(y, folder, self.pannel.sub))

    def update(self):
        global RELOAD
        if RELOAD: 
            self.gen()
            RELOAD=False

        for project in self.projects:
            project.update()

    def render(self):
        self.pannel.render(render_sub=False)
        for project in self.projects:
            project.render()
        self.pannel.sub.render()

class Project:
    def __init__(self, y, folderName, sub: SubScreen): #folder name is NAME.engine
        self.pos = Vector2D(10, y)
        self.size = Vector2D(Net.screen_size.x-180, 50)
        self.Psub = sub
        self.pannel = Pannel(self.pos.x, self.pos.y, self.size.x, self.size.y, [54, 61, 74], "black", displaySurface=sub.screen, parent=sub)

        self.folderName = folderName
        self.name = folderName.split(".")[0]
        r = pygame.Rect(sub.pos.x, sub.pos.y-200, sub.dim.x, sub.dim.y+200)
        self.btn = self.pannel.add_object(btn(0, 0, self.size.x, self.size.y, [54, 61, 74], borderColor="white", minw=-1, maxw=2, sub=self.pannel.sub, toggle=True, toggleRect=r))
        self.pannel.add_object(Text(35, self.name, (255, 255, 255), Vector2D(5, self.size.y//2), "midleft"))

        self.op: Options = None

    def update(self):
        self.btn.update()
        if self.btn.pressed and not self.op:
            self.op = Options(self.name)
        elif not self.btn.pressed and self.op:
            self.op = None
        if self.op: self.op.update()

    def render(self):
        self.pannel.render()
        if self.op: self.op.render()

class Options:
    def __init__(self, name):
        self.name = name
        self.pos = Vector2D(Net.screen_size.x-140, 90)
        self.size = Vector2D(120, Net.screen_size.y-110)
        self.pan = Pannel(self.pos.x, self.pos.y, self.size.x, self.size.y, [54, 61, 74], "black", displaySurface=Net.screen)
        self.pan.add_object(Text(35, "options:", (255, 255, 255), Vector2D(5, 5), "topleft"))

        i=self.size.x-20
        self.btns: dict[str, btn] = {
            "edit": self.pan.add_object(btn(10, 40, i, 30, [29, 34, 41], "Edit", (255, 255, 255), 30, "white", -1, 2, sub=self.pan.sub)),
            "run": self.pan.add_object(btn(10, 80, i, 30, [29, 34, 41], "Run", (255, 255, 255), 30, "white", -1, 2, sub=self.pan.sub)),
            "build": self.pan.add_object(btn(10, 120, i, 30, [29, 34, 41], "Build", (255, 255, 255), 30, "white", -1, 2, sub=self.pan.sub)),
                        
            "del": self.pan.add_object(btn(10, 200, i, 30, [29, 34, 41], "Delete", (255, 0, 0), 30, "white", -1, 2, sub=self.pan.sub)),
        }

    def update(self):
        for btn in self.btns.values():
            btn.update()

        #btn interactions
        if self.btns["run"].pressed: self._run()
        elif self.btns["edit"].pressed: self._edit()
        elif self.btns["build"].pressed: BuildProject(self.name+".engine").gen()
        elif self.btns["del"].pressed: self._del()

    def _run(self):
        BuildProject(self.name+".engine").gen()
        Runner(self.name+".engine")

    def _edit(self):
        RunEditor(self.name)

    def _del(self):
        global RELOAD
        path = f"{Net.save_dir}/{self.name}.engine"
        #remove folder if exists
        if os.path.exists(path):
            shutil.rmtree(path)
            RELOAD = True

    def render(self):
        self.pan.render()
