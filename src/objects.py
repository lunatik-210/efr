
from loader import load_image

class PigOnTractor:
    def __init__(self):
        self.image, self.rect = load_image('PigOnTractor.png', 'alpha')
        self.x, self.y = (300, 300)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class BigWheel:
    pass

class SmallWheel:
    pass