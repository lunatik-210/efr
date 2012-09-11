
########## System libs ##########
import sys
#################################

######### Game logic ############
import engine
import states
#################################

def start(fullscreen_option=True, debug_option=False):
    game = engine.Game('Escape from Russia', (800, 600))
    #game.set_full_screen(fullscreen_option)
    game.run(states.MainMenu(game, debug_option))

if __name__ == "__main__":
    """Command line flags:
        [-f] fullscreen mode on
        [-w] window mode on
        [-d] debug mode on
    """

    fullscreen_option = True
    debug_option = True # Actually False as default, but who cares <_<

    argv = sys.argv
    for arg in argv:
        if arg == "-d":
            debug_option = True
        elif arg == "-f":
            fullscreen_option = True
        elif arg == "-w":
            fullscreen_option = False

    start(fullscreen_option, debug_option)
