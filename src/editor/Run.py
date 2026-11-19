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

    print("[Editor] - loaded successfully")
    while True:
        if Net.update(False):
            Project.save()
            break
        if Project.RLD_SELF: 
            Project.RLD_SELF = False
            Project.load()

        #debug
        if Keys.is_pressed(Keys.escape): 
            Project.save()
            break

        #update
        top.update()
        tabs.update()

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




