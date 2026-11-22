import pygame
import os
import sys
import json

from ..Net import Net

class BuildProject:
    def __init__(self, folder):
        self.write = FileData()
        self.buildFilePath = f"{Net.save_dir}/{folder}/build.py"
        self.projectPath = f"{Net.save_dir}/{folder}/_project.json"
        self.cache_path = f"{Net.save_dir}/{folder}/_buildcache_/"
        self.folder = folder

    def gen(self):
        #gen cache
        self.cache_gen()
        #gens main file
        self.message()
        self.gen_imports()
        #gen cache
        self.add_cache()

        self.gen_entry()


        self.writeFile()

    def add_cache(self):
        for file in os.listdir(self.cache_path):
            with open (self.cache_path+file, "r") as f:
                data = f.read()
            self.write.line(data)

    def cache_gen(self):
        #scenes
        for scene in os.listdir(f"{Net.save_dir}/{self.folder}/scenes/"):
            with open(f"{Net.save_dir}/{self.folder}/scenes/{scene}", "r") as f:
                data = json.load(f)
            self.gen_cache_scene_file(data, scene.split(".")[0])
        #objs
        for obj in os.listdir(f"{Net.save_dir}/{self.folder}/objects/"):
                with open(f"{Net.save_dir}/{self.folder}/objects/{obj}", "r") as f:
                    data = json.load(f)
                self.gen_cache_obj_file(data, obj.split(".")[0])

    def gen_cache_scene_file(self, data, name):
        if not data["dirty"]: return #dont rewrite non changed files
        line = FileData()
        path = f"{self.cache_path}{name}.py"
        #line.line("#THIS IS A BUILD FILE, PLEASE DONT EDIT")
        for i in data["code"]:
            #if i.split(" ")[0] in ["import", "from"]: continue
            if i == "": continue
            line.line(i)

        line.nl()
        line.save(path)
    def gen_cache_obj_file(self, data, name):
        if not data["dirty"]: return #dont rewrite non changed files
        line = FileData()
        path = f"{self.cache_path}{name}.py"
        #line.line("#THIS IS A BUILD FILE, PLEASE DONT EDIT")
        for i in data["code"]:
            #if i.split(" ")[0] in ["import", "from"]: continue
            if i == "": continue
            line.line(i)

        line.nl()
        line.save(path)

    def message(self):
        self.write.line("########################")
        self.write.line("#-BUILT FILE, DONT EDIT-#")
        self.write.line("########################")

    def gen_imports(self):
        self.write.line("from PyScene import *")
        self.write.line("import os")
        self.write.line("import sys")
        self.write.line("import pygame", 1)

    def gen_entry(self):
        with open(self.projectPath, "r") as f:
            data = json.load(f)
        i = data["window"]
        self.write.nl()
        self.write.line("#ENTRY / START POINT", 1)
        self.write.line(f"Game.init({i['width']}, {i['height']}, '{i['title']}', "
            f"{i['bg_color']}, {i['fps']}, {i['fullscreen']}, True) #-starts game-", 1)
        #if there is a scene
        if data["main_scene"] != "":
            self.write.line(f"{data['main_scene']}()", 1)
        else: self.write.line("print('No start scene defined')#-no main scene-", 1)

        #region DEBUG / Test
        self.write.line("test()")

        self.write.line("Game.Run(True)", 1)

    def writeFile(self):
        with open(self.buildFilePath, "w") as f:
            f.write(self.write.data)


class FileData:
    def __init__(self):
        self.data = ""
        self.tab = 0
    def line(self, text, nl=0):
        if self.tab > 0: self.data += "\t"*self.tab
        self.data += f"{text}\n"
        if nl > 0: self.nl(nl)
    def nl(self, count=1):
        self.data += "\n"*count
    def save(self, path):
        with open(path, "w") as f:
            f.write(self.data)
