import pygame

from PyScene import Vector2D

from ...Net import Net, _project
from ...utils import *
from ._tab import Tab

Project: _project = None

class ManagerTab(Tab):
    def __init__(self, x, sub, rect, project: _project):
        
        super().__init__(x, "Tabs", sub, rect)
        global Project
        Project = project
        self.__type = "manager"

        #other stuff
        self.pan = Pannel(0, Net._y, Net.screen_size.x, Net.screen_size.y-Net._y, [29, 34, 41], displaySurface=Net.screen)
        self.pan.add_object(Line(0, 2, self.pan.dim.x, 2))

        self.scenes = None
        self.objs = None

        self.gen()

    def gen(self):
        self.pan.remove_object(self.scenes)
        self.pan.remove_object(self.objs)

        self.scenes = self.pan.add_object(FilePannel(True, "scene", self.pan))
        self.objs = self.pan.add_object(FilePannel(False, "object", self.pan))

    def _update(self):
        self.scenes.update()
        self.objs.update()

        if Project.RLD_MANAGER: self.gen()

    def _render(self):
        self.pan.render()

class FilePannel:
    def __init__(self, left, _type_, screen: Pannel):
        w = 800
        if left: x = 10
        else: x = Net.screen_size.x-10-w
        self.pos = Vector2D(x, 10)
        self.pan = Pannel(x, self.pos.y, w, Net.screen_size.y-20, [33, 38, 46], "black", displaySurface=screen.sub.screen, parent=screen.sub)
        
        self.objs: list[OBJ] = []
        
        y = 50
        for name in getattr(Project, _type_+"s"):
            self.objs.append(self.pan.add_object(OBJ(y, self.pan, name, _type_)))
            y+=60

        self.type = _type_
        self._rect = pygame.Rect(x, self.pos.y, w, Net.screen_size.y-20)
        num = len(getattr(Project, _type_+"s"))
        self.pan.add_object(Rect(1, 1, self.pan.dim.x-2, 43, [33, 38, 46]))
        self.pan.add_object(Text(45, f"{_type_}s ({num} made)", "white", Vector2D(w//2, 10), "midtop"))
        self.pan.add_object(Line(0, 45, self.pan.dim.x, 45))

        self.create = self.pan.add_object(btn(5, 5, 35, 35, [29, 34, 41], "+", "white", 40, "white", -1, 2, sub=self.pan.sub))
        self.cting = False
        self.input: CreateFile = None

    def handle_scroll(self, s=Net.scroll*10):
        if s == 0: return

        #if can scroll
        if s > 0:
            if self.objs[0].pos.y+s > 70: return
        else:
            if self.objs[-1].pos.y+s < self.pan.dim.y-70: return
            
        for obj in self.objs:
            obj.scroll(s)

    def _create(self):
        if self.cting: return
        self.cting = True
        self.handle_scroll(9999) #scroll to bottom
        self.input = self.pan.add_object(CreateFile(self.objs[-1].pos.y+60, self.pan))

    def update(self):
        mpos = pygame.mouse.get_pos()
        if self.create.update() or (self._rect.collidepoint(mpos) and (Keys.is_held(Keys.control) and Keys.is_pressed(Keys.a))):
            self._create()

        self.handle_scroll()

    def render(self, screen):
        self.pan.render()

class CreateFile:
    def __init__(self, y, pan: Pannel):
        self.y = y
        self.input = TextInput(btn(
            0, y, pan.dim.x, 50, "black",
            font=40, toggle=True, sub=pan.sub
        ))
        self.done = False

    def update(self):
        self.input.update()

    def render(self, screen):
        self.input.render(screen)

class OBJ:
    def __init__(self, y, pan: Pannel, name, _type_):
        self.pos = Vector2D(0, y)
        self.size = Vector2D(pan.dim.x, 50)
        self.pan = Pannel(self.pos.x, self.pos.y, self.size.x, self.size.y, (25, 26, 27), "black", displaySurface=pan.sub.screen, parent=pan.sub)

        self.name = name
        self.type = _type_

        self.pan.add_object(Text(35, self.name, "white", Vector2D(10, self.size.y//2), "midleft"))

    def scroll(self, amount):
        self.pos.y += amount
        self.pan.pos.y += amount
        self.pan.sub.pos.y += amount

    def update(self):
        pass

    def render(self, screen):
        self.pan.render()

