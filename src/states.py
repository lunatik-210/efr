
import pygame
from pygame.locals import *

if not pygame.font: logging.warning('Warning, fonts disabled')
if not pygame.mixer: logging.warning('Warning, sound disabled')

import engine
from button import Button
from loader import load_image

class MainMenu(engine.State):
    def init(self):
        image = load_image('just_to_test_screen.png') # pygame.image.load(os.path.join("./", 'just_to_test_screen.png')).convert()      
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
                if event.key == K_ESCAPE:
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
                if event.key == K_ESCAPE:
                    return MainMenu(self.game, self.debug)
        
class Game(engine.State):
    def init(self):
        image = load_image('bg_800x600.png')
        self.screen.blit(image[0], (0,0))

    def event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return engine.Quit(self.game, self.debug)
            elif event.type == pygame.KEYDOWN: 
                if event.key == K_ESCAPE:
                    return MainMenu(self.game, self.debug)

