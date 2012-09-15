
import pygame
from pygame.locals import *

if not pygame.font: logging.warning('Warning, fonts disabled')
if not pygame.mixer: logging.warning('Warning, sound disabled')

import engine
import objects
import webbrowser

from scene import Scene
from loader import load_image

UPDATESCENE = USEREVENT+1

class MainMenu(engine.State):
    def init(self):
        image = load_image('main_menu.jpg')     
        self.screen.blit(image[0], (0,0))

        self.start_button = pygame.Rect((440, 30), (340, 115))
        self.about_button = pygame.Rect((320, 155), (250, 90))
        self.exit_button = pygame.Rect((240, 255), (160, 60))
        self.pyweek15_button = pygame.Rect((155, 310), (85, 45))

    def event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return engine.Quit(self.game, self.debug)
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    return engine.Quit(self.game, self.debug)
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.start_button.collidepoint( mouse[0], mouse[1] ):
                    return Game(self.game, self.debug)
                elif self.about_button.collidepoint( mouse[0], mouse[1] ):
                    return About(self.game, self.debug)
                elif self.exit_button.collidepoint( mouse[0], mouse[1] ):
                    return engine.Quit(self.game, self.debug)
                elif self.pyweek15_button.collidepoint( mouse[0], mouse[1] ):
                    webbrowser.open_new("http://www.pyweek.org/15/")

class About(engine.State):
    def init(self):
        self.screen.blit(load_image('about_menu.png')[0], (0,0))
        self.pyweek15_button = pygame.Rect((155, 310), (75, 40))

    def event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return engine.Quit(self.game, self.debug)
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    return MainMenu(self.game, self.debug)
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.pyweek15_button.collidepoint( mouse[0], mouse[1] ):
                    webbrowser.open_new("http://www.pyweek.org/15/")

class Speed:
    def __init__(self,):
        self.levels = [0, 25, 20, 10]
        self.consumption = [ 0, 0.30, 0.04, 0.02 ]
        self.level = 0
        pygame.time.set_timer(UPDATESCENE, self.value())

    def up(self):
        if self.level < len(self.levels)-1:
            self.level += 1
        pygame.time.set_timer(UPDATESCENE, self.value())

    def down(self):
        if self.level > 0:
            self.level -= 1
        pygame.time.set_timer(UPDATESCENE, self.value())

    def value(self):
        return self.levels[self.level]

    def stop(self):
        self.level = 0
        pygame.time.set_timer(UPDATESCENE, self.value())        

    def gas_consumption(self):
        return self.consumption[self.level]

class Game(engine.State):
    def init(self):
        self.image = load_image('bg_800x600.png')
        self.screen.blit(self.image[0], (0,0))

        self.speed = Speed()

        self.player = objects.PigOnTractor((250, 300), self.speed)

        self.police = objects.Police((-100, 300), self.speed)

        self.scene = Scene(self.player)

        for i in range(200):
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
                    self.speed.down()
                elif event.key == pygame.K_RIGHT:
                    self.speed.up()

            elif event.type == UPDATESCENE:
                self.do_scene()
                self.player.consume_gas()

        self.player.event(events)

    def update(self, passed_time):
        self.player.update()
        self.scene.update()
        self.police.update()
        if self.player.status() == 'arrested':
            return GameOver(self.game, self.debug, 'game_over_arrested.png', self.player.get_score())
        elif self.player.status() == 'died':
            return GameOver(self.game, self.debug, 'game_over_die.png', self.player.get_score())

    def paint(self):
        self.screen.blit(self.image[0], (0,0))
        self.scene.draw(self.screen)
        self.player.draw(self.screen)
        self.police.draw(self.screen)
        
class GameOver(engine.State):
    def __init__(self, game, debug, game_over_screen_name, player_score):
        self.game_over_screen_name = game_over_screen_name
        self.player_score = player_score
        engine.State.__init__(self, game, debug)

    def init(self):
        image = load_image(self.game_over_screen_name)  
        self.screen.blit(image[0], (0,0))

        myFont = pygame.font.SysFont("Calibri", 55)
        self.screen.blit(myFont.render("Your final score %s!" % self.player_score, 1, (0,0,0)), (200, 550))

    def event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return engine.Quit(self.game, self.debug)
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    return MainMenu(self.game, self.debug)
