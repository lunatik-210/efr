import pygame
from loader import load_image
from config import *
import pyganim
import gradients

objects = { 'tree' : ['tree1', 'tree2', 'tree3', 'tree4'], 
            'cloud' : ['cloud1', 'cloud2', 'cloud3', 'cloud4'], 
            'road' : ['roadborder1', 'roadborder2', 'roadborder3'],
            'roadr' : ['roadborder1r', 'roadborder2r', 'roadborder3r'],
            'horizon' : ['horizon1', 'horizon2', 'horizon3'],
            'house' : ['gas_station', 'workshop']
          }

class Button():
    def __init__(self, screen, name, coords):
        self.image, self.rect = load_image(name, -1)
        self.rect = screen.blit( self.image, coords )

    def pressed(self, mouse):
        return self.rect.collidepoint( mouse[0], mouse[1] )

class Object:
    def __init__(self, coords, name, x_bias = 0):
        self.x, self.y = coords
        self.name = name
        self.x_bias = x_bias
        self.image, self.rect = load_image( self.name + '.png' , 'alpha')

    def draw(self, screen):
        self.rect = screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.x += self.x_bias

    def event(self, events):
        pass

class ProgressBar(pygame.Surface):
    def __init__(self, start_col, end_color):
        self.width = 120
        self.height = 15
        self.border = 1
        self.start_col, self.end_color = start_col, end_color
        self.sub_width = self.width-self.border*2
        self.sub_height = self.height-self.border*2
        self.value = self.sub_width
        pygame.Surface.__init__(self, (self.width, self.height))

    def fill(self):
        pygame.Surface.fill(self, (0,0,0))
        pygame.Surface.fill(self, (255,255,255), pygame.Rect((self.border,self.border), (self.sub_width, self.sub_height)))

    def update(self, value):
        self.fill()
        if value > 1:
            self.value = (int)(self.sub_width * value / 100.0)
            pygame.Surface.blit(self, gradients.horizontal((self.value, self.sub_height), self.start_col, self.end_color), (self.border,self.border))

class PlayerBar:
    def __init__(self):
        self.score = 100
        self.health = 100
        self.gas = 100
        self.health_bar = ProgressBar((100, 0, 0, 100), (255, 0, 0, 255))
        self.gas_bar = ProgressBar((0, 0, 0, 100), (0, 0, 0, 255))
        self.surface = pygame.Surface((190, 130))
        #self.surface.fill((117, 152, 203))

    def draw(self, screen):
        self.surface.fill((117, 152, 203))
        
        self.surface.blit( load_image('dollar.png', 'alpha')[0], (0, 0) )

        myFont = pygame.font.SysFont("Calibri", 70)
        self.surface.blit(myFont.render("%s" % self.score , 1, (0,0,0)), (70, 15))

        myFont = pygame.font.SysFont("Calibri", 20)
        self.surface.blit(myFont.render("Health" , 10, (0,0,0)), (5, 85))
        self.surface.blit(myFont.render("Gas" , 1, (0,0,0)), (5, 105))

        self.surface.blit( self.health_bar, (60, 85) )
        self.surface.blit( self.gas_bar, (60, 105) )

        screen.blit( self.surface, (600, 10) )

    def update(self):
        self.health_bar.update((int)(self.health))
        self.gas_bar.update((int)(self.gas))

class PigOnTractor():
    def __init__(self, coords, speed):
        
        self.x, self.y = coords
        self.image, self.rect = load_image('tractor_body.png', 'alpha')

        self.player_bar = PlayerBar()
        self.speed = speed

        self.car_image, self.car_rect = load_image('car_body.png', 'alpha')
        self.width, self.height = self.image.get_size()
        self.rate = 5
        self.peter, self.peter_rect = load_image('peter_open_front.png', 'alpha')

        self.moveUp = self.moveDown = self.moveLeft = self.moveRight = False

        self.big_wheel = BigWheel()
        self.small_wheel = SmallWheel()
        self.smoke = Smoke()

    def test_action(self, obj):
        if obj.name == 'gas_station':
            if obj.rect.contains(self.peter_rect) and self.rect.contains(self.rect):
                if self.player_bar.gas < 100 and self.player_bar.score > 0:
                    self.player_bar.gas += 1.5
                    self.player_bar.score -= 1
        elif obj.name == 'workshop':
            if obj.rect.contains(self.peter_rect) and self.rect.contains(self.rect):
                if self.player_bar.health < 100 and self.player_bar.score > 0:
                    self.player_bar.health += 2
                    self.player_bar.score -= 1

    def get_score(self):
        return self.player_bar.score

    def status(self):
        if self.player_bar.gas < 0:
            return 'arrested'
        if self.player_bar.health <0:
            return 'died'
        return None

    def consume_gas(self):
        self.player_bar.gas -= self.speed.gas_consumption()

    def draw(self, screen):
        self.player_bar.draw(screen)

        self.peter_rect = screen.blit(self.peter, (self.x-14, self.y-20))
        self.rect = screen.blit(self.image, (self.x, self.y))

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
        self.player_bar.update()

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
