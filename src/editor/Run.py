import pygame
import os
import sys
import json
import ctypes

from PyScene import Vector2D

from ..Net import Net, _project
from ..utils import *

from ..build.Build import BuildProject
from ..runner.Run import Runner

from .TopBar import TopBar
from .Tabs.Manager import TabManager

Project: _project = None

def RunEditor(projectName):
    global Project

    #basics
    i = 2
    Net.screen_size = Vector2D(1280*i, 672*i)
    Net.screen = pygame.display.set_mode(Net.screen_size.to_int(), pygame.SCALED | pygame.RESIZABLE)
    Net.screen_rect = Net.screen.get_rect()

    pygame.display.set_caption(f"AnotherEngine Editor - {projectName}")
    hwnd = pygame.display.get_wm_info()["window"]
    ctypes.windll.user32.ShowWindow(hwnd, 3)  # 3 = SW_MAXIMIZE

    Project = _project(projectName)

    top = TopBar(Project)
    tabs = TabManager(Project)
    open_last_tabs(tabs)

    

    print("[Editor] - loaded successfully")
    while True:
        if Net.update(False):
            save_open_tabs(tabs) 
            Project.save()
            break
        if Project.RLD_SELF: 
            Project.RLD_SELF = False
            Project.load()

        #debug
        if Keys.is_pressed(Keys.escape):
            save_open_tabs(tabs) 
            Project.save()
            break

        #update
        top.update()
        tabs.update()

        if Project.OPN_TB["check"]:
            tabs.open(Project.OPN_TB["name"], Project.OPN_TB["type"])
            Project.OPN_TB["check"] = False
        elif Project.CLS_TB["check"]:
            tabs.close(Project.CLS_TB["name"], Project.CLS_TB["type"])
            Project.CLS_TB["check"] = False

        Net.screen.fill((0, 0, 0))

        #render
        top.render()
        tabs.render()

        #pygame.draw.circle(Net.screen, (255, 0, 0), (0, Net.screen_size.y), 10) #test screen size(s)
        Net.mouse_cursor()
        pygame.display.flip()

    #return
    print("[Editor] - returning to manager...")
    Net.manager().Run()

def save_open_tabs(tabs: TabManager):
    Project.project["lastOpen"] = []
    Project.project["changed"] = True
    for i in range(3, len(tabs.tabs)):
        Project.project["lastOpen"].append(tabs.tabs[i]._name)
        print(i)

def open_last_tabs(tabs: TabManager):
    for name in Project.project["lastOpen"]:
        _type = "scene" if name in Project.scenes else "object"
        tabs.open(name, _type)
    tabs._deactivate(len(tabs.tabs)-1)
    tabs._activate(2)





