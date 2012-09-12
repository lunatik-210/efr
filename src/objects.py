
from loader import load_image

objects = { 'tree' : ['tree1', 'tree2', 'tree3', 'tree4'], 
            'cloud' : ['cloud1', 'cloud2', 'cloud3', 'cloud4'], 
          }


class Object:
    def __init__(self, coords, name, is_solid):
        self.x, self.y = coords
        self.name = name
        self.is_solid = is_solid
        self.image, self.rect = load_image( name + '.png' , 'alpha')

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class PigOnTractor:
    def __init__(self):
        self.image, self.rect = load_image('pig_on_tractor.png', 'alpha')
        self.width, self.height = self.image.get_size()
        self.x, self.y = (300, 300)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class BigWheel:
    pass

class SmallWheel:
    pass