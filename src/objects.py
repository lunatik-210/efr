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

    def event(self, events):
        pass

class PigOnTractor(Object):
    def __init__(self, coords):
        Object.__init__(self, coords, 'tractor_body', True)
        #self.image, self.rect = load_image('tractor_body.png', 'alpha')

        self.car_image, self.car_rect = load_image('car_body.png', 'alpha')
        self.width, self.height = self.image.get_size()
        self.rate = 5
        self.peter, self.peter_rect = load_image('peter_open_front.png', 'alpha')

        self.moveUp = self.moveDown = self.moveLeft = self.moveRight = False

        self.big_wheel = BigWheel()
        self.small_wheel = SmallWheel()
        self.smoke = Smoke()

    def draw(self, screen):
        screen.blit(self.peter, (self.x-14, self.y-20))
        screen.blit(self.image, (self.x, self.y))

        self.big_wheel.draw(screen, (self.x, self.y+52))
        self.small_wheel.draw(screen, (self.x+95, self.y+77))
        self.smoke.draw(screen, (self.x+8, self.y-65))
        
    def change_car(self):
        self.image = self.car_image
        self.rect = self.car_rect
        # TODO:
        # hide smoke
        # make new wheels instead others

    def event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_UP:
                    self.moveUp = True
                    self.moveDown = False
                elif event.key == pygame.K_DOWN:
                    self.moveDown = True
                    self.moveUp = False
                elif event.key == pygame.K_LEFT:
                    self.moveLeft = True
                    self.moveRight = False
                elif event.key == pygame.K_RIGHT:
                    self.moveRight = True
                    self.moveLeft = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.moveUp = False
                elif event.key == pygame.K_DOWN:
                    self.moveDown = False
                elif event.key == pygame.K_LEFT:
                    self.moveLeft = False
                elif event.key == pygame.K_RIGHT:
                    self.moveRight = False

    def update(self):
        if self.moveUp or self.moveDown or self.moveLeft or self.moveRight:
            if self.moveUp:
                if self.y > ROAD_BORDER_TOP:
                    self.y -= self.rate
            if self.moveDown:
                if self.y < ROAD_BORDER_BOTTOM:
                    self.y += self.rate
            if self.moveLeft:
                #self.x -= self.rate
                pass
            if self.moveRight:
                #self.x += self.rate
                pass

        if self.x < 0:
            self.x = 0
        if self.x > WINDOW_WIDTH - self.width:
            self.x = WINDOW_WIDTH - self.width
        if self.y < 0:
            self.y = 0
        if self.y > WINDOW_HEIGHT - self.height:
            self.y = WINDOW_HEIGHT - self.height
            self.change_car()

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
