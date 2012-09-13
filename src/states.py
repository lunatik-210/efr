
import pygame
from pygame.locals import *

if not pygame.font: logging.warning('Warning, fonts disabled')
if not pygame.mixer: logging.warning('Warning, sound disabled')

import engine
import objects

from scene import Scene
from loader import load_image

class MainMenu(engine.State):
    def init(self):
        image = load_image('just_to_test_screen.png')     
        self.screen.blit(image[0], (0,0))

        self.start_button = objects.Button(self.screen, "start.png", (250, 100))
        self.about_button = objects.Button(self.screen, "about.png", (250, 200))
        self.exit_button = objects.Button(self.screen, "exit.png", (250, 300))
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

class Game(engine.State):
    def init(self):
        self.image = load_image('bg_800x600.png')
        self.screen.blit(self.image[0], (0,0))

        self.player = objects.PigOnTractor()
        self.moveUp = self.moveDown = self.moveLeft = self.moveRight = False

        self.scene = Scene()

        for i in range(150):
            self.do_scene()

    def do_scene(self):
        self.scene.generate()
        self.scene.bias()
        self.scene.clean()        

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

        self.do_scene()

    def paint(self):
        self.screen.blit(self.image[0], (0,0))
        self.scene.draw(self.screen)
        self.player.draw(self.screen)
        
