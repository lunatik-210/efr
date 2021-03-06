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

from loader import load_image
from random import uniform
from random import choice
import objects

from config import *

class Scene:
    
    #########################
    # Pixels for main screen
    # Sky 0 - 208
    # Ground 208 - 280
    # Road 280 - 412 - 544
    # Ground 544 - 600
    #########################

    def __init__(self, player):
        self.passed_distance = 0
        self.road_border_id = 0

        self.borders = (WINDOW_WIDTH, WINDOW_HEIGHT)

        self.player = player
        self.objects = { 1 : [], 2 : [], 3 : [], 4 : [] }
        self.solid_objects = { 1 : [], 2 : [], 3 : [], 4 : [] }
        
        self.x_bias = 5

    # draw scene to the screen
    def draw(self, screen):
        for lvl in range(1,len(self.objects)+1):
            for obj in self.objects[lvl]:
                obj.draw(screen)

        for lvl in range(1,len(self.solid_objects)+1):
            for obj in self.solid_objects[lvl]:
                obj.draw(screen)

    # must clean from objects which has gone from the screen
    def clean(self):
        if self.passed_distance % 300:      
            for lvl in range(1,len(self.objects)+1):
                for obj in self.objects[lvl]:
                    if obj.x < -800:
                        self.objects[lvl].remove(obj)

            for lvl in range(1,len(self.solid_objects)+1):
                for obj in self.solid_objects[lvl]:
                    if obj.x < -800:
                        self.solid_objects[lvl].remove(obj)

    # generate new sequence of objects for the scene
    def generate(self):
        if self.passed_distance % 4500 == 0:
            house_n = (int)(uniform(0, 2))
            self.solid_objects[1].append( objects.Object( (800, 190), objects.objects['house'][house_n] ) )
        if self.passed_distance % 1600 == 0:
            for i in range(int(uniform(1,3))):
                self.solid_objects[3].append( objects.Hedgehog( (800, int(uniform(300, 500))), (300, 500)) )
        if self.passed_distance % 3200 == 0:
            self.solid_objects[4].append( objects.Box( (800, choice([250, 330, 380, 440]) )))
        if self.passed_distance % 1900 == 0:
            if int(uniform(0,2)) == 1:
                self.solid_objects[2].append( objects.Object( (int(uniform(800, 900)), int(uniform(300, 500))), 'cleft' ) )
            self.solid_objects[2].append( objects.Object( (800, int(uniform(300, 500))), 'cleft' ) )
        if self.passed_distance % 12000 == 0:
            self.solid_objects[1].append( objects.Object( (800, 160), 'repairstation'))

        if self.passed_distance % 130 == 0:
            self.objects[1].append( objects.Object( (800, 400), 'double_line' ) )
        if self.passed_distance % 160 == 0:
            gen_y = (int)(uniform(120, 175))
            tree_n = (int)(uniform(0, 4))
            self.objects[3].append( objects.Object( (800, gen_y), objects.objects['tree'][tree_n] ) )
        if self.passed_distance % 250 == 0:
            gen_y = (int)(uniform(0, 150))
            tree_n = (int)(uniform(0, 4))
            self.objects[2].append( objects.Object( (800, gen_y), objects.objects['cloud'][tree_n], (int)(uniform(-3, -1) ) ) )
        if self.passed_distance % 800 == 0:
            self.objects[1].append( objects.Object( (800, 480), objects.objects['road'][self.road_border_id]) )
            self.objects[1].append( objects.Object( (800, 240), objects.objects['roadr'][self.road_border_id]) )
            self.objects[1].append( objects.Object( (800, 180), objects.objects['horizon'][self.road_border_id]) )
            self.road_border_id = (self.road_border_id + 1) % 3
        if self.passed_distance % 170 == 0:
            self.objects[1].append( objects.Object( (800, 340), 'line' ) )
            self.objects[1].append( objects.Object( (800, 470), 'line' ) )

    # just bias whole scene to the left
    def bias(self):
        self.passed_distance = ( self.passed_distance + self.x_bias )
        for lvl in range(1,len(self.objects)+1):
            for obj in self.objects[lvl]:
                obj.x -= self.x_bias

        for lvl in range(1,len(self.solid_objects)+1):
            for obj in self.solid_objects[lvl]:
                obj.x -= self.x_bias
    
    def update(self):
        for lvl in range(1,len(self.objects)+1):
            for obj in self.objects[lvl]:
                obj.update()

        for lvl in range(1,len(self.solid_objects)+1):
            for obj in self.solid_objects[lvl]:
                obj.update()
                self.player.test_action(obj)      
                    
