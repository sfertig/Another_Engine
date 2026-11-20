import pygame

from PyScene import Vector2D

from ...Net import Net, _project
from ...utils import *
from ._tab import Tab

Project: _project = None

class ManagerTab(Tab):
    def __init__(self, x, sub, rect, project: _project):
        global Project
        Project = project

        super().__init__(x, "Tabs", sub, rect, Project, False)

        self._type_ = "manager"

        #other stuff
        self.pan = Pannel(0, Net._y, Net.screen_size.x, Net.screen_size.y-Net._y, [29, 34, 41], displaySurface=Net.screen)
        self.pan.add_object(Line(20, 2, self.pan.dim.x-20, 2))

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

        if Project.RLD_MANAGER: 
            self.gen()
            Project.RLD_MANAGER = False 

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

    def handle_scroll(self, s):
        s = s * 10  # Multiply the scroll speed here
        
        if s == 0 or len(self.objs) == 0: 
            return
            
        # Check bounds before scrolling
        if s > 0: #down
            if self.objs[0].pos.y + s > 70: 
                return
        else: #up
            if self.objs[-1].pos.y + s < self.pan.dim.y - 500: 
                return
                
        for obj in self.objs:
            obj.scroll(s)

    def _create(self):
        if self.cting: return
        self.cting = True
        self.handle_scroll(-9999) #scroll to bottom
        if len(self.objs) > 0: y = self.objs[-1].pos.y
        else: y = -10
        self.input = self.pan.add_object(CreateFile(y+60, self.pan))

    def _new(self):
        text = self.input.input.btn.text.text
        
        self.pan.remove_object(self.input)
        self.cting = False
            
        if Project.valid_name(text): 
            Project.new(text, self.type)
            Project.RLD_MANAGER = True

    def update(self):

        if self.input: 
            if self.input.update(): self._new()

        mpos = pygame.mouse.get_pos()
        if self.create.update() or (self._rect.collidepoint(mpos) and (Keys.is_held(Keys.control) and Keys.is_pressed(Keys.a))):
            self._create()

        if self._rect.collidepoint(mpos): self.handle_scroll(Net.scroll)

        for obj in self.objs: obj.update()

    def render(self, screen):
        self.pan.render()

class CreateFile:
    def __init__(self, y, pan: Pannel):
        self.y = y
        self.input = TextInput(btn(
            0, y, pan.dim.x, 50, (25, 26, 27),
            font=40, toggle=True, sub=pan.sub
        ))
        self.input.btn.pressed = True
        Net.click = False

    def update(self):
        self.input.update()
        return not self.input.btn.pressed

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
        
        self.open = self.pan.add_object(btn(self.size.x-260, 5, 80, self.size.y-10
            , (29, 34, 41), "Open", "white", 40, "white", -1, 2, sub=self.pan.sub))
        self._del = self.pan.add_object(btn(self.size.x-160, 5, 150, self.size.y-10
                    , (29, 34, 41), "Del (enter)", "red", 40, "red", -1, 2, sub=self.pan.sub))

    def scroll(self, amount):
        self.pos.y += amount
        self.pan.pos.y += amount
        self.pan.sub.pos.y += amount

    def update(self):
        self.open.update()
        self._del.update()

        if self._del.hovered and Keys.is_pressed(Keys.enter): 
            Project.Delete(self.name, self.type)
            Project.RLD_MANAGER = True
        elif self.open.pressed:
            Project.OPN_TB["check"] = True
            Project.OPN_TB["name"] = self.name
            Project.OPN_TB["type"] = self.type

    def render(self, screen):
        self.pan.render()

