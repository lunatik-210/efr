
import pygame

from pygame.locals import *

import os

def load_image(name, colorkey=None):
    data_py = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.normpath(os.path.join(data_py, '..', 'data'))
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
