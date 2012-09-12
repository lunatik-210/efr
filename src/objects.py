import pygame
from loader import load_image

objects = { 'tree' : ['tree1', 'tree2', 'tree3', 'tree4'], 
            'cloud' : ['cloud1', 'cloud2', 'cloud3', 'cloud4'], 
          }


class Object:
    def __init__(self, coords, name, is_solid):
        self.x, self.y = coords
        self.name = name
        self.is_solid = is_solid
        self.image, self.rect = load_image( name + '.png' , 'alpha')

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class PigOnTractor:
    def __init__(self):
        self.image, self.rect = load_image('pig_on_tractor.png', 'alpha')
        self.width, self.height = self.image.get_size()
        self.x, self.y = (300, 300)
        self.rate = 4

        self.big_wheel = BigWheel(self.x+15, self.y+70)
        self.small_wheel = SmallWheel(self.x+115, self.y+95)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.big_wheel.draw(screen)
        self.small_wheel.draw(screen)

    def update(self, moveUp, moveDown, moveLeft, moveRight):
        # TODO: get constants from global settings
        WINDOWWIDTH = 800
        WINDOWHEIGHT = 600

        if moveUp or moveDown or moveLeft or moveRight:
            if moveUp:
                self.y -= self.rate
                self.big_wheel.y -= self.rate 
                self.small_wheel.y -= self.rate 
            if moveDown:
                self.y += self.rate
                self.big_wheel.y += self.rate
                self.small_wheel.y += self.rate
            if moveLeft:
                self.x -= self.rate
                self.big_wheel.x -= self.rate
                self.small_wheel.x -= self.rate
            if moveRight:
                self.x += self.rate
                self.big_wheel.x += self.rate
                self.small_wheel.x += self.rate

        # TODO: set right limit for player movements
        if self.x < 0:
            self.x = 0
            self.big_wheel.x = 0
            self.small_wheel.x = 0
        if self.x > WINDOWWIDTH - self.width:
            self.x = WINDOWWIDTH - self.width
            self.big_wheel.x = WINDOWWIDTH - self.width
            self.small_wheel.x = WINDOWWIDTH - self.width
        if self.y < 0:
            self.y = 0
            self.big_wheel.y = 0
            self.small_wheel.y = 0
        if self.y > WINDOWHEIGHT - self.height:
            self.y = WINDOWHEIGHT - self.height
            self.big_wheel.y = WINDOWWIDTH - self.height
            self.small_wheel.y = WINDOWWIDTH - self.height

        # self.big_wheel.update()
        # self.small_wheel.update()


class Wheel:
    def __init__(self, x, y):
        self.image, self.rect = load_image('big_wheel.png', 'alpha')
        self.base_image = self.image
        self.width, self.height = self.image.get_size()
        self.x, self.y = (x, y)

    def update(self):
        self.rotate()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def rotate(self):
        print "rotation"
        self.image = pygame.transform.rotate(self.base_image, -10.0)
        self.rect = self.image.get_rect()


class BigWheel(Wheel):
    def __init__(self, x, y):
        self.image, self.rect = load_image('big_wheel.png', 'alpha')
        self.base_image = self.image
        self.width, self.height = self.image.get_size()
        self.x, self.y = (x, y)

class SmallWheel(Wheel):
    def __init__(self, x, y):
        self.image, self.rect = load_image('small_wheel.png', 'alpha')
        self.base_image = self.image
        self.width, self.height = self.image.get_size()
        self.x, self.y = (x, y)

