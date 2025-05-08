import pygame
import math
import numpy as np

from settings import *
from supercover_line import supercover_line

class Observers(pygame.sprite.Sprite):
    def __init__(self, world, background, fov, pos ,color):   
        #input pos array of [x,y, orientation]

        self.images = []
        self.rects = []

        for i in range(len(pos)):
            self.images.append(pygame.Surface([ROBOT_WIDTH,ROBOT_WIDTH]))
            self.images[i].fill(color)
            self.rects = self.images[i].get_rect(center=(pos[i][0],pos[i][1]))