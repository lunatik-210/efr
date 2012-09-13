
import pygame
from pygame.locals import *

if not pygame.font: logging.warning('Warning, fonts disabled')
if not pygame.mixer: logging.warning('Warning, sound disabled')

import engine
import objects

from button import Button
from loader import load_image
from random import uniform

class MainMenu(engine.State):
    def init(self):
        image = load_image('just_to_test_screen.png')     
        self.screen.blit(image[0], (0,0))

        self.start_button = Button(self.screen, "start.png", (250, 100))
        self.about_button = Button(self.screen, "about.png", (250, 200))
        self.exit_button = Button(self.screen, "exit.png", (250, 300))
        return

    def event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return engine.Quit(self.game, self.debug)
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    return engine.Quit(self.game, self.debug)
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.start_button.pressed(mouse):
                    return Game(self.game, self.debug)
                elif self.about_button.pressed(mouse):
                    return About(self.game, self.debug)
                elif self.exit_button.pressed(mouse):
                    return engine.Quit(self.game, self.debug)

class About(engine.State):
    def init(self):
        self.screen.fill((0,0,0))
        myFont = pygame.font.SysFont("Calibri", 100)
        myText = myFont.render("About", 1, (255,255,255))
        self.screen.blit(myText, (300, 100))

    def event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return engine.Quit(self.game, self.debug)
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    return MainMenu(self.game, self.debug)

class Scene:
    
    #########################
    # Pixels for main screen
    # Sky 0 - 208
    # Ground 208 - 280
    # Road 280 - 412 - 544
    # Ground 544 - 600
    #########################

    def __init__(self):
        self.area_map = { 'sky' : (0, 208),
                          'top_ground' : (208, 280),
                          'road' : (280, 544),
                          'bottom_ground' : (544, 600) }

        self.passed_distance = 0

        self.borders = (800, 600)
        self.objects = []

    # draw scene to the screen
    def draw(self, screen):
        for obj in self.objects:
            obj.draw(screen)

    # must clean from objects which has gone from the screen
    def clean(self):
        for obj in self.objects:
            if obj.x < -100:
                self.objects.remove(obj)

    # generate new sequence of objects for the scene
    def generate(self):
        if self.passed_distance % 130 == 0:
            self.objects.append( objects.Object( (800, 400), 'double_line', False ) )
        if self.passed_distance % 160 == 0:
            gen_y = (int)(uniform(120, 175))
            tree_n = (int)(uniform(0, 4))
            self.objects.append( objects.Object( (800, gen_y), objects.objects['tree'][tree_n], False ) )
        if self.passed_distance % 250 == 0:
            gen_y = (int)(uniform(0, 150))
            tree_n = (int)(uniform(0, 4))
            self.objects.append( objects.Object( (800, gen_y), objects.objects['cloud'][tree_n], False ) )

    # just bias whole scene to the left
    def bias(self):
        x_bias = 5
        self.passed_distance = ( self.passed_distance + x_bias ) % 800
        for obj in self.objects:
            obj.x -= x_bias

class Game(engine.State):
    def init(self):
        self.image = load_image('bg_800x600.png')
        self.screen.blit(self.image[0], (0,0))

        self.player = objects.PigOnTractor()
        self.moveUp = self.moveDown = self.moveLeft = self.moveRight = False

        self.scene = Scene()

    def event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return engine.Quit(self.game, self.debug)

            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    return MainMenu(self.game, self.debug)
                if event.key == K_UP:
                    self.moveUp = True
                    self.moveDown = False
                elif event.key == K_DOWN:
                    self.moveDown = True
                    self.moveUp = False
                elif event.key == K_LEFT:
                    self.moveLeft = True
                    self.moveRight = False
                elif event.key == K_RIGHT:
                    self.moveRight = True
                    self.moveLeft = False

            elif event.type == KEYUP:
                if event.key == K_UP:
                    self.moveUp = False
                elif event.key == K_DOWN:
                    self.moveDown = False
                elif event.key == K_LEFT:
                    self.moveLeft = False
                elif event.key == K_RIGHT:
                    self.moveRight = False

    def action(self, passed_time):
        self.player.update(self.moveUp, self.moveDown, self.moveLeft, self.moveRight)

        self.scene.generate()
        self.scene.bias()
        self.scene.clean()

    def paint(self):
        self.screen.blit(self.image[0], (0,0))
        self.scene.draw(self.screen)
        self.player.draw(self.screen)
        
