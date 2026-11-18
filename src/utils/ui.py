import pygame
from PyScene import Vector2D

from .subscreen import SubScreen
from ..Net import Net
from .input import Keys

import inspect

#region Pannel
class Pannel:
    def __init__(self, x, y, w, h, bgColor, borderColor=None, borderPadding=2, displaySurface: pygame.Surface = None, parent=None):
        self.pos = Vector2D(x, y)
        self.dim = Vector2D(w, h)
        self.bgColor = bgColor
        self.borderColor = borderColor or bgColor
        self.borderPadding = borderPadding
        self._screen = displaySurface
        self.parent = parent  # Reference to parent SubScreen
        self.sub = SubScreen(x, y, w, h, bgColor, displaySurface, parent)
        self.screen = self.sub.screen

        self.objs = [] # List to hold objects added to the panel for rendering

        #resizing
        self.minw=0
        self.minh=0
        self.maxw=0
        self.maxh=0
        self.resizable=False
        self.hovered = False
        self.rszx=False
        self.rszy=False

        self.crszx=False
        self.crszy=False

        self.up = None
        self.down = None
        self.left = None
        self.right = None

        self.orgin_mpos = None
        self.active_resize = False
        self.already = False

    def set_resize(self, minw, minh, maxw, maxh, crszx=True, crszy=True):
        self.minw = minw
        self.minh = minh
        self.maxw = maxw
        self.maxh = maxh
        self.resizable = True
        self.crszx = crszx
        self.crszy = crszy

        self._update_hitboxes()

    def _update_hitboxes(self):
        p = 5
        self.up = pygame.Rect(0, 0, self.dim.x, p)
        self.down = pygame.Rect(0, self.dim.y - p, self.dim.x, p)
        self.left = pygame.Rect(0, 0, p, self.dim.y)
        self.right = pygame.Rect(self.dim.x - p, 0, p, self.dim.y)

    def update(self):
        if not self.resizable:
            return

        # 1. Start drag on initial click while hovering an edge
        if not self.active_resize:
            self.hovered = False
            mpos = self.sub.local_mouse_pos().to_int()
            if self.crszy:
                if self.up.collidepoint(mpos): self.hovered = "up"
                elif self.down.collidepoint(mpos): self.hovered = "down"
            if self.crszx:
                if self.left.collidepoint(mpos): self.hovered = "left"
                elif self.right.collidepoint(mpos): self.hovered = "right"

            if self.hovered and Net.mouse_down and not self.already:
                self.active_resize = True
                self.active_edge = self.hovered
                self.origin_mpos = pygame.mouse.get_pos()
                self.origin_pos = Vector2D(self.pos.x, self.pos.y)
                self.origin_dim = Vector2D(self.dim.x, self.dim.y)
            elif Net.mouse_down and not self.hovered:
                self.already = True

        # 2. Stop drag when mouse button is released
        if not Net.mouse_down:
            self.active_resize = False
            self.active_edge = None
            self.already = False

        # 3. Maintain the resize cursor while hovering OR actively dragging
        current_edge = self.active_edge if self.active_resize else self.hovered
        if current_edge in ["up", "down"]:
            Net.cursor = pygame.SYSTEM_CURSOR_SIZENS
        elif current_edge in ["left", "right"]:
            Net.cursor = pygame.SYSTEM_CURSOR_SIZEWE

        # 4. Calculate new dimensions and position using global mouse delta
        if self.active_resize:
            gx, gy = pygame.mouse.get_pos()
            dx = gx - self.origin_mpos[0]
            dy = gy - self.origin_mpos[1]

            if self.active_edge == "right":
                self.dim.x = max(self.minw, min(self.origin_dim.x + dx, self.maxw))

            elif self.active_edge == "left":
                new_w = max(self.minw, min(self.origin_dim.x - dx, self.maxw))
                self.pos.x = self.origin_pos.x + (self.origin_dim.x - new_w)
                self.dim.x = new_w

            elif self.active_edge == "down":
                self.dim.y = max(self.minh, min(self.origin_dim.y + dy, self.maxh))

            elif self.active_edge == "up":
                new_h = max(self.minh, min(self.origin_dim.y - dy, self.maxh))
                self.pos.y = self.origin_pos.y + (self.origin_dim.y - new_h)
                self.dim.y = new_h

            # Update hitboxes and SubScreen surface to match new pos/dim
            self._update_hitboxes()
            self.sub = SubScreen(self.pos.x, self.pos.y, self.dim.x, self.dim.y, self.bgColor, self._screen, self.parent)
            self.screen = self.sub.screen


    def render(self, cam: Vector2D = Vector2D(0, 0), render_sub=True):
        self.update()
        self.sub.clear()

        pygame.draw.rect(self.screen, self.borderColor, (0, 0, self.dim.x, self.dim.y), self.borderPadding)

        for obj in self.objs:
            obj.render(self.screen)

        self.sub.render(cam)

    def add_object(self, obj):
        if hasattr(obj, 'render'):
            if obj not in self.objs and "screen" in inspect.signature(obj.render).parameters:
                self.objs.append(obj)
        return obj
    
    def remove_object(self, obj):
        if obj in self.objs:
            self.objs.remove(obj)



#region Text


class Text:
    def __init__(self, font, text, color, pos=Vector2D(0, 0), align="center"):
        self.pos = pos
        self.font = font
        if type(font) == int: self.font = pygame.font.Font(None, font)
        self.text = text
        self.color = color
        self.align = align
        self.surface = None
        self.rect = None

        self._update_surface()

    def _update_surface(self):
        """Internal method to re-render surface only when text changes."""
        self.surface = self.font.render(str(self.text), False, self.color)
        self._apply_alignment()

    def _apply_alignment(self):
        """Safely positions the rect based on single or multi-coordinate alignment."""
        xy = self.pos.to_int()  # Assuming this returns (x, y)
        
        # Group single-coordinate attributes by which axis they care about
        x_aligns = {"left", "right", "centerx", "x"}
        y_aligns = {"top", "bottom", "centery", "y"}

        if self.align in x_aligns:
            # Create a default rect at (0,0), then assign the specific X coordinate
            self.rect = self.surface.get_rect()
            setattr(self.rect, self.align, xy[0])
        elif self.align in y_aligns:
            # Create a default rect at (0,0), then assign the specific Y coordinate
            self.rect = self.surface.get_rect()
            setattr(self.rect, self.align, xy[1])
        else:
            # Multi-coordinate alignments (center, topleft, etc.) safely accept the full tuple
            self.rect = self.surface.get_rect(**{self.align: xy})

    def set_text(self, new_text, color=None):
        """Only call this when the string actually changes!"""
        if color is not None:
            self.color = color
        if new_text != self.text:
            self.text = new_text
            self._update_surface()

    def set_pos(self, new_pos: Vector2D):
        self.pos = new_pos
        self._apply_alignment()

    def render(self, screen):
        screen.blit(self.surface, self.rect)

#region Btn

class btn:
    def __init__(self, x, y, w, h, bgColor, text="", textColor=(255, 255, 255), font=30, 
                 borderColor=None, minw=2, maxw=5, toggle=False, toggleRect=None, sub=None, 
                 bor=-1, toggleSelf=True):
        self.pos = Vector2D(x, y)
        self.dim = Vector2D(w, h)
        self.bg = bgColor
        self.border = borderColor or bgColor
        self.minw = minw
        self.maxw = maxw
        self.w = minw
        self.b = bor

        self.rect = pygame.Rect(x, y, w, h)
        self.toggle = toggle
        self.hovered = False
        self.pressed = False
        self.tRect = toggleRect or Net.screen_rect
        self.sub = sub

        self.text = Text(font, text, textColor, Vector2D(x + w / 2, y + h / 2))
        self.font = font
        self.Tcolor = textColor

        self.toggleSelf = toggleSelf

    def update(self):
        if self.toggle: self._toggle()
        else: self._hover()
        return self.pressed

    def _mpos_hover(self):
        if self.sub: mpos = self.sub.local_mouse_pos().to_int()
        else: mpos = pygame.mouse.get_pos()

        self.hovered = self.rect.collidepoint(mpos)
        #print(mpos, self.hovered)

    def _toggle(self):
        self._mpos_hover()
        if self.pressed: self.w = self.maxw
        else: self.w = self.minw
        if self.tRect.collidepoint(pygame.mouse.get_pos()): 
            if Net.click and self.hovered: 
                if self.toggleSelf: self.pressed = not self.pressed
                else: self.pressed = True
            elif Net.click and not self.hovered: self.pressed = False

    def _hover(self):
        self._mpos_hover()
        if self.hovered: self.w = self.maxw
        else: self.w = self.minw
        if Net.click and self.hovered: self.pressed = True
        else: self.pressed = False

    def render(self, screen):
        pygame.draw.rect(screen, self.bg, self.rect, 0, self.b)
        pygame.draw.rect(screen, self.border, self.rect, self.w, self.b)
        self.text.render(screen)

#region Text Input

class TextInput:
    def __init__(self, btn):
        self.btn = btn
        self.buffer = 0

    def update(self):
        self.btn.update()

        if self.btn.pressed:
            if Keys.is_pressed(Keys.enter) or Keys.is_pressed(Keys.escape): self.btn.pressed = False
            else:
                text = self.btn.text.text
                #done = False
                for event in Net.events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE: continue #text = text[:-1]
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE: continue
                        else: text += event.unicode
                if Keys.is_held(Keys.backspace) and self.buffer == 0: 
                    text = text[:-1]
                    self.buffer = 15
                elif not Keys.is_held(Keys.backspace): self.buffer = 0
                if text != self.btn.text.text: self.btn.text.set_text(text)

    def render(self, screen):
        self.btn.render(screen)

#region Line

class Line:
    def __init__(self, x1, y1, x2, y2, color=(0, 0, 0), w=1):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.w = w

    def render(self, screen):
        pygame.draw.line(screen, self.color, (self.x1, self.y1), (self.x2, self.y2), self.w)

#class Rect

class Rect:
    def __init__(self, x, y, w, h, color, width=0, b=1):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.width = width
        self.b = b

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, self.width, self.b)

