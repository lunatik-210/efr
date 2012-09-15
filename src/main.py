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

########## System libs ##########
import sys
#################################

######### Game logic ############
import engine
import states
#################################

######### Game config ############
from config import *
#################################


def start(fullscreen_option=True, debug_option=False):
    game = engine.Game('Escape from Russia', (WINDOW_WIDTH, WINDOW_HEIGHT))
    # game.set_full_screen(fullscreen_option)
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
