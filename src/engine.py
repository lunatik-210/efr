
import pygame

class State:
    """Base State, inherit it if you want new one"""
    def __init__(self, game, debug=False):
        self.game = game
        self.screen = self.game.screen
        self.debug = debug
        self.init()

    def init(self):
        """Overload it ro make any initializations"""
        return

    def paint(self):
        """Overload to paint any to the screen (use self.screen in your program)"""
        return

    def event(self, events):
        """Overload to process sequence of events"""
        return """If you want to go to another state return it here"""

    def action(self, passed_time):
        """Overload to do some action"""
        return 

class Quit(State):
    """A state to quit the state engine."""
    
    def init(self): 
        self.game.quit = True

class Game:
    """ Game engine, use it to start the game """
    def __init__(self, caption, screen_size=(1024, 768), fps = 30):
        pygame.init()
        pygame.display.set_caption(caption)
        self.screen_size = screen_size
        self.screen = None
        self.set_full_screen(False)
        self.fps = fps

    def set_fps(self, fps):
        self.fps = fps

    def set_full_screen(self, fullscreen_option):
        modes = pygame.display.list_modes(32)
        if modes and fullscreen_option:
            self.screen = pygame.display.set_mode(modes[0], pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN, 32)
        else:
            self.screen = pygame.display.set_mode(self.screen_size)

    def run(self, state):
        self.quit = False
        self.state = state

        clock = pygame.time.Clock()
        while not self.quit:
            passed_time = clock.tick(self.fps)
            self.__loop(passed_time)

        self.__quit()

    def __loop(self, passed_time):
        s = self.state.event(pygame.event.get())
        if s: self.state = s
        self.state.action(passed_time)
        self.state.paint()
        pygame.display.update()

    def __quit(self):
        pygame.display.quit()
        pygame.quit()