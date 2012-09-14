
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

class Speed:
    def __init__(self,):
        self.levels = [0, 25, 20, 10]
        self.consumption = [ 0.08, 0.05, 0.03, 0.01 ]
        self.level = 0

    def up(self):
        if self.level < len(self.levels)-1:
            self.level += 1
        return self.value()

    def down(self):
        if self.level > 0:
            self.level -= 1
        return self.value()

    def value(self):
        return self.levels[self.level]

    def gas_consumption(self):
        return self.consumption[self.level]

class Game(engine.State):
    def init(self):
        self.image = load_image('bg_800x600.png')
        self.screen.blit(self.image[0], (0,0))

        self.UPDATESCENE = USEREVENT+1

        self.speed = Speed()

        pygame.time.set_timer(self.UPDATESCENE, self.speed.value())

        self.player = objects.PigOnTractor((250, 300), self.speed)

        self.scene = Scene(self.player)

        for i in range(160):
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
                elif event.key == pygame.K_LEFT:
                    pygame.time.set_timer(self.UPDATESCENE, self.speed.down())
                elif event.key == pygame.K_RIGHT:
                    pygame.time.set_timer(self.UPDATESCENE, self.speed.up())

            elif event.type == self.UPDATESCENE:
                self.do_scene()
                self.player.consume_gas()

        self.player.event(events)

    def update(self, passed_time):
        self.player.update()
        self.scene.update()

    def paint(self):
        self.screen.blit(self.image[0], (0,0))
        self.scene.draw(self.screen)
        self.player.draw(self.screen)
        
