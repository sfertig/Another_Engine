import pygame
import os
import sys
import json

from PyScene import Vector2D

from ..Net import Net, _project
from ..utils import *

Project: _project = None

def RunEditor(projectName):
    global Project

    Net.reset()
    #basics
    Net.screen_size = Vector2D(1920, 1080)
    Net.screen = pygame.display.set_mode(Net.screen_size.to_int(), pygame.FULLSCREEN | pygame.SCALED)
    Net.screen_rect = Net.screen.get_rect()
    pygame.display.set_caption(f"AnotherEngine Editor - {projectName}")

    Project = _project(projectName)

    while True:
        Net.update()

        #debug
        if Keys.is_pressed(Keys.escape): break

        Net.screen.fill((0, 0, 0))

        pygame.display.flip()

    #return
    Net.manager().Run()



