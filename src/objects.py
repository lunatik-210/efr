#############################################################################
#    Copyright (C) 2012 Andrew Lapin, Alexander Gudulin, Michael Turusov
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Contacts: andrew.d.lapin@gmail.com
#############################################################################

import pygame
import loader

from loader import load_image, load_sound
from config import *

import pyganim
import gradients

import random
import os 

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

class Box(Object):
    def __init__(self, coords, delay = 0.1):
        Object.__init__(self, coords, 'roadbox')
        self.brokenbox_image = load_image('brokenbox.png', 'alpha')[0]
        self.status = None

    def update(self):
        if self.status == 'died':
            self.image = self.brokenbox_image

class Hedgehog(Object):
    def __init__(self, coords, borders, delay = 0.1):
        Object.__init__(self, coords, 'hedgehog')
        self.left_standing = load_image('hedgehog_l.png', 'alpha')[0]
        self.right_standing = load_image('hedgehog.png', 'alpha')[0]
        self.bloodshit = load_image('bloodshit.png', 'alpha')[0]
        self.animations = {}
        self.animations['right_walk'] = pyganim.PygAnimation([(os.path.join(loader.data_dir, 'hedgehog.png'), delay),
                                                              (os.path.join(loader.data_dir, 'hedgehog_run.png'), delay)])
        self.animations['left_walk']  = pyganim.PygAnimation([(os.path.join(loader.data_dir, 'hedgehog_l.png'), delay),
                                                              (os.path.join(loader.data_dir, 'hedgehog_run_l.png'), delay)])
        self.animation_manager = pyganim.PygConductor(self.animations)
        self.status = None
        self.borders = borders
        self.direction_x = random.uniform(-3, 3)
        self.direction_y = random.uniform(-3, 3)

    def update(self):
        if self.status == 'died':
            return
        if not self.borders[0] < self.y < self.borders[1]:
            self.direction_y *= -1

        self.x += self.direction_x
        self.y += self.direction_y

        if self.direction_x > 0:
            self.animation_manager.play()
            self.status = 'right_walk'
        elif self.direction_x < 0:
            self.animation_manager.play()
            self.status = 'left_walk'
        elif self.direction_x == 0:
            self.animation_manager.stop()
            if self.status == 'right_walk':
                self.status = 'right_standing'
            elif self.status == 'left_walk':
                self.status = 'left_standing'

    def draw(self, screen):
        if self.status == 'right_walk':
            self.rect = self.animations[self.status].blit(screen, (self.x, self.y))
        elif self.status == 'left_walk':
            self.rect = self.animations[self.status].blit(screen, (self.x, self.y))
        elif self.status == 'right_standing':
            self.rect = screen.blit(self.right_standing, (self.x, self.y))
        elif self.status == 'left_standing':
            self.rect = screen.blit(self.left_standing, (self.x, self.y))
        elif self.status == 'died':
            self.rect = screen.blit(self.bloodshit, (self.x, self.y))

class ProgressBar(pygame.Surface):
    def __init__(self, start_col, end_color, sizes = (120, 15, 1)):
        self.width = sizes[0]
        self.height = sizes[1]
        self.border = sizes[2]
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
        self.score = 0
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

class Police:
    def __init__(self, coords, speed):
        self.x, self.y = coords
        self.image, self.rect = load_image('police.png', 'alpha')
        self.left_wheel = SmallWheel()
        self.right_wheel = SmallWheel()
        self.speed = speed
        self.police_bar = ProgressBar((0, 0, 255, 150), (200, 0, 0, 255), (290, 40, 1))
        self.distance = 0
        self.status = None

    def draw(self, screen):
        self.rect = screen.blit(self.image, (self.x, self.y))

        self.left_wheel.draw(screen, (self.x+47, self.y+102))
        self.right_wheel.draw(screen, (self.x+170, self.y+102))

        screen.blit( self.police_bar, (10, 10) )
        myFont = pygame.font.SysFont("Calibri", 30)
        screen.blit(myFont.render("Cops are about to grab your", 1, (0, 0, 0)), (20, 20))

    def update(self):
        if self.speed.value() == 0:
            self.distance += 0.4
        elif self.speed.value() == 25:
            self.distance += 0.3
        elif self.speed.value() == 20:
            self.distance += 0.2
        elif self.speed.value() == 10:
            self.distance -= 0.1
            self.gap_down()

        if self.distance < 0:
            self.distance = 0
        if self.distance > 100:
            self.distance = 100

        if self.distance > 70:
            self.gap_up()

        self.police_bar.update(self.distance)
        self.left_wheel.update(self.speed)
        self.right_wheel.update(self.speed)

        if self.x > 130:
            self.status = 'arrest'

    def gap_up(self):
        if self.x < 300:
            self.x += 2

    def gap_down(self):
        if self.x > -300:
            self.x -= 3

class PigOnTractor():
    def __init__(self, coords, speed):
        
        self.x, self.y = coords
        self.image_car, self.rect = load_image('tractor_body.png', 'alpha')
        self.image = self.image_car
        self.image_bldzr, self.rect_bldzr = load_image('bulldozer.png', 'alpha')
        self.width, self.height = self.image.get_size()
        self.rate = 5

        self.player_bar = PlayerBar()
        self.speed = speed

        self.car_image, self.car_rect = load_image('car_body.png', 'alpha')
        self.peter, self.peter_rect = load_image('peter_open_front.png', 'alpha')

        self.moveUp = self.moveDown = self.moveLeft = self.moveRight = False

        self.big_wheel = BigWheel()
        self.small_wheel = SmallWheel()
        self.smoke = Smoke()

        self.is_bulldozer = False
        self.drop_coin_sound = Music('drop_coin.ogg')
        self.drop_box_sound = Music('drop_box.ogg')
        self.hedgehog_sound = Music('hedgehog_oops.ogg')

    def test_action(self, obj):
        if obj.name == 'gas_station':
            if obj.rect.contains(self.peter_rect) and self.speed.value() == 0:
                if self.player_bar.gas < 100 and self.player_bar.score > 0:
                    self.player_bar.gas += 1.5
                    self.player_bar.score -= 1
                    self.drop_coin_sound.play()

        elif obj.name == 'workshop':
            if obj.rect.contains(self.peter_rect) and self.speed.value() == 0:
                if self.player_bar.health < 100 and self.player_bar.score > 0:
                    self.player_bar.health += 1.5
                    self.player_bar.score -= 1
                    self.drop_coin_sound.play()

        elif obj.name == 'hedgehog' and obj.status != 'died':
            if self.small_wheel.rect != None and self.small_wheel.rect.colliderect(obj.rect):
                obj.status = 'died'
                if self.is_bulldozer:
                    self.player_bar.score += 3
                else:
                    self.player_bar.health -= 1
                    self.player_bar.score += 5
                    self.speed.down()
                self.hedgehog_sound.play()

        elif obj.name == 'cleft':
            if (self.small_wheel.rect != None and self.small_wheel.rect.colliderect(obj.rect)):
                if self.is_bulldozer:
                    self.player_bar.health -= 1
                else:
                    self.player_bar.health -= 2

        elif obj.name == 'roadbox' and obj.status != 'died':
            if self.rect.colliderect(obj.rect):
                obj.status = 'died'
                if self.is_bulldozer:
                    self.player_bar.health -= 4
                else:
                    self.player_bar.health -= 8
                self.player_bar.score += random.randint(10, 30)
                self.drop_box_sound.play()
                self.speed.stop()

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

        #   Car:                Bulldozer:
        #       0. Pig              0. Wheels + smoke
        #       1. Car              1. Bulldozer
        #       2. Wheels + smoke

        if not self.is_bulldozer:
            self.peter_rect = screen.blit(self.peter, (self.x-14, self.y-20))
            self.image = self.image_car
            self.rect = screen.blit(self.image, (self.x, self.y))

        self.big_wheel.draw(screen, (self.x, self.y+52))
        self.small_wheel.draw(screen, (self.x+95, self.y+77))
        self.smoke.draw(screen, (self.x+8, self.y-65))

        if self.is_bulldozer:
            self.image = self.image_bldzr
            self.rect = screen.blit(self.image, (self.x, self.y))
            
    def change_car(self):
        self.is_bulldozer = not self.is_bulldozer

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

        self.big_wheel.update(self.speed)
        self.small_wheel.update(self.speed)
        self.smoke.update(self.speed)


class Animation:
    def __init__(self):
        self.rect = None

    def update(self, speed):
        if speed.value() == 0:
            self.image.pause()
        else:
            self.image.play()

    def draw(self, screen, (x, y)):
        self.rect = self.image.blit(screen, (x, y))


class BigWheel(Animation):
    def __init__(self, delay=0.1):
        Animation.__init__(self)
        self.delay = delay
        self.image = pyganim.PygAnimation([(os.path.join(loader.data_dir, 'big_wheel1.png'), self.delay),
                                          (os.path.join(loader.data_dir, 'big_wheel2.png'), self.delay),
                                          (os.path.join(loader.data_dir, 'big_wheel3.png'), self.delay)])

class SmallWheel(Animation):
    def __init__(self, delay=0.1):
        Animation.__init__(self)
        self.delay = delay
        self.image = pyganim.PygAnimation([(os.path.join(loader.data_dir, 'small_wheel1.png'), self.delay),
                                          (os.path.join(loader.data_dir, 'small_wheel2.png'), self.delay),
                                          (os.path.join(loader.data_dir, 'small_wheel3.png'), self.delay)])

class Smoke(Animation):
    def __init__(self, delay=0.1):
        Animation.__init__(self)
        self.delay = delay
        self.image = pyganim.PygAnimation([(os.path.join(loader.data_dir, 'smoke1.png'), self.delay),
                                          (os.path.join(loader.data_dir, 'smoke2.png'), self.delay),
                                          (os.path.join(loader.data_dir, 'smoke3.png'), self.delay)])

class Music():
    def __init__(self, soundfile):
        self.soundfile = soundfile
        # pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)

    def play(self):
        sound = load_sound(self.soundfile)
        sound.play(0) # Sound.play(loops=0, maxtime=0, fade_ms=0)

