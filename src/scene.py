
from loader import load_image
from random import uniform
import objects

class Scene:
    
    #########################
    # Pixels for main screen
    # Sky 0 - 208
    # Ground 208 - 280
    # Road 280 - 412 - 544
    # Ground 544 - 600
    #########################

    def __init__(self):
        self.passed_distance = 0
        self.road_border_id = 0

        self.borders = (800, 600)
        self.objects = { 1 : [], 2 : [] }

    # draw scene to the screen
    def draw(self, screen):
        for lvl in range(1,3):
            for obj in self.objects[lvl]:
                obj.draw(screen)

    # must clean from objects which has gone from the screen
    def clean(self):
        if self.passed_distance % 300:      
            for lvl in range(1,3):
                for obj in self.objects[lvl]:
                    if obj.x < -800:
                        self.objects[lvl].remove(obj)

    # generate new sequence of objects for the scene
    def generate(self):
        if self.passed_distance % 130 == 0:
            self.objects[1].append( objects.Object( (800, 400), 'double_line', False ) )
        if self.passed_distance % 160 == 0:
            gen_y = (int)(uniform(120, 175))
            tree_n = (int)(uniform(0, 4))
            self.objects[2].append( objects.Object( (800, gen_y), objects.objects['tree'][tree_n], False ) )
        if self.passed_distance % 250 == 0:
            gen_y = (int)(uniform(0, 150))
            tree_n = (int)(uniform(0, 4))
            self.objects[2].append( objects.Object( (800, gen_y), objects.objects['cloud'][tree_n], False, (int)(uniform(-3, -1) ) ) )
        if self.passed_distance % 800 == 0:
            self.objects[1].append( objects.Object( (800, 480), objects.objects['road'][self.road_border_id], False) )
            self.objects[1].append( objects.Object( (800, 240), objects.objects['roadr'][self.road_border_id], False) )
            self.objects[1].append( objects.Object( (800, 180), objects.objects['horizon'][self.road_border_id], False) )
            self.road_border_id = (self.road_border_id + 1) % 3
        if self.passed_distance % 170 == 0:
            self.objects[1].append( objects.Object( (800, 340), 'line', False ) )
            self.objects[1].append( objects.Object( (800, 470), 'line', False ) )

    # just bias whole scene to the left
    def bias(self):
        x_bias = 5
        self.passed_distance = ( self.passed_distance + x_bias ) % 800
        for lvl in range(1,3):
            for obj in self.objects[lvl]:
                obj.x -= x_bias
                obj.update()