import pygame
from loader import load_image
from config import *
import pyganim


objects = { 'tree' : ['tree1', 'tree2', 'tree3', 'tree4'], 
            'cloud' : ['cloud1', 'cloud2', 'cloud3', 'cloud4'], 
            'road' : ['roadborder1', 'roadborder2', 'roadborder3'],
            'roadr' : ['roadborder1r', 'roadborder2r', 'roadborder3r'],
            'horizon' : ['horizon1', 'horizon2', 'horizon3'],
          }

class Button():
    def __init__(self, screen, name, coords):
        self.image, self.rect = load_image(name, -1)
        self.rect = screen.blit( self.image, coords )

    def pressed(self, mouse):
        return self.rect.collidepoint( mouse[0], mouse[1] )

class Object:
    def __init__(self, coords, name, is_solid, x_bias = 0):
        self.x, self.y = coords
        self.name = name
        self.is_solid = is_solid
        self.x_bias = x_bias
        self.image, self.rect = load_image( name + '.png' , 'alpha')

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.x += self.x_bias

class PigOnTractor:
    def __init__(self):
        self.image, self.rect = load_image('pig_on_tractor.png', 'alpha')
        self.width, self.height = self.image.get_size()
        self.x, self.y = (300, 300)
        self.rate = 5

        self.big_wheel = BigWheel()
        self.small_wheel = SmallWheel()
        self.smoke = Smoke()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.big_wheel.draw(screen, (self.x+15, self.y+70))
        self.small_wheel.draw(screen, (self.x+115, self.y+95))
        self.smoke.draw(screen, (self.x+25, self.y-50))
        

    def update(self, moveUp, moveDown, moveLeft, moveRight):
        if moveUp or moveDown or moveLeft or moveRight:
            if moveUp:
                self.y -= self.rate
            if moveDown:
                self.y += self.rate
            if moveLeft:
                self.x -= self.rate
            if moveRight:
                self.x += self.rate

        if self.x < 0:
            self.x = 0
        if self.x > WINDOW_WIDTH - self.width:
            self.x = WINDOW_WIDTH - self.width
        if self.y < 0:
            self.y = 0
        if self.y > WINDOW_HEIGHT - self.height:
            self.y = WINDOW_HEIGHT - self.height

        self.big_wheel.update()
        self.small_wheel.update()
        self.smoke.update()


class Animation:
    def __init__(self):
        pass

    def update(self):
        self.image.play()

    def draw(self, screen, (x, y)):
        self.image.blit(screen, (x, y))


class BigWheel(Animation):
    def __init__(self, delay=0.1):
        self.delay = delay
        self.image = pyganim.PygAnimation([('../data/big_wheel1.png', self.delay),
                                          ('../data/big_wheel2.png', self.delay),
                                          ('../data/big_wheel3.png', self.delay)])

class SmallWheel(Animation):
    def __init__(self, delay=0.1):
        self.delay = delay
        self.image = pyganim.PygAnimation([('../data/small_wheel1.png', self.delay),
                                          ('../data/small_wheel2.png', self.delay),
                                          ('../data/small_wheel3.png', self.delay)])

class Smoke(Animation):
    def __init__(self, delay=0.1):
        self.delay = delay
        self.image = pyganim.PygAnimation([('../data/smoke1.png', self.delay),
                                           ('../data/smoke2.png', self.delay),
                                           ('../data/smoke3.png', self.delay)])
