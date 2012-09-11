
import pygame
from loader import load_image

class Button():
    """Class used to create a button, use setCords to set 
        position of topleft corner. Method pressed() returns
        a boolean and should be called inside the input loop."""
    def __init__(self, screen, name, coords):
        #pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(name, -1)
        self.rect = screen.blit( self.image, coords )

    def pressed(self, mouse):
        return self.rect.collidepoint( mouse[0], mouse[1] )
