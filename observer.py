import pygame
import math
import numpy as np

from settings import *
from supercover_line import supercover_line

class Observers(pygame.sprite.Sprite):
    def __init__(self, map, fov, pos ,color, background):   
        #input pos array of [x,y, orientation]
        self.pos_grid= pos

        self.map = map

        self.images = []
        self.rects = []

        for i in range(len(pos)):
            self.images.append(pygame.Surface([ROBOT_WIDTH,ROBOT_WIDTH]))
            self.images[i].fill(color)
            self.rects = self.images[i].get_rect(center=(pos[i][0],pos[i][1]))

        self.background = pygame.Surface((background.get_width(),background.get_height()),pygame.SRCALPHA)

        self.fov = fov

    def vision(self):

        self.visionmap = np.zeros([2,self.map.shape[0], self.map.shape[1]])

        for i in range(len(self.pos_grid)):
            print("current ang: "+str(i))
            for theta in np.arange(0,self.fov,1):
                theta_adjusted = theta +self.pos_grid[i][2]
                # theta_adjusted = theta
                end_x, end_y = OB_VIEW_DIST*math.cos(math.radians(theta_adjusted)), OB_VIEW_DIST*math.sin(math.radians(theta_adjusted))
                endp = [(int((end_x) + self.pos_grid[i][0])), (int((end_y) + self.pos_grid[i][1]))]
                line = supercover_line(self.pos_grid[i],endp)

                for j in range(len(line)):
                    x, y = line[j][1],line[j][0]

                    if x >= self.map.shape[0] or y >= self.map.shape[1] or x<0 or y<0: # disreguard out of range readings
                        continue

                    if self.map[x,y] == 0: #if wall is found stop searching the lines
                        break
                    else:
                        self.visionmap[0,x,y] += (OB_VIEW_DIST-j)*0.1*VISION_COST  #TODO map these to each robot
                        self.visionmap[1,x,y] =  i  ### TODO make this hold multiple robots (maybe new variable)
        # print(self.visionmap)
        return self.visionmap

    def add_observers_tomap(self, map):
        self.ob_map = map

        for i in range(len(self.pos_grid)):
            x, y = self.pos_grid[i][0], self.pos_grid[i][1]
            
            self.ob_map[y,x] = 3
        
        return self.ob_map
    

    def def_vision_map(self):
        self.surfgrid = []
        print(str(self.visionmap.shape[1]) + str(self.visionmap.shape[2]))

        for i in range(self.visionmap.shape[1]):
            for j in range(self.visionmap.shape[2]):
                if self.visionmap[0,i,j] > 0:
                    # self.surfgrid.append([i,j,self.visionmap[i,j]])
                    self.surfgrid.append([pygame.Surface(pygame.Rect((ROBOT_WIDTH*i, ROBOT_WIDTH*j, ROBOT_WIDTH, ROBOT_WIDTH)).size, pygame.SRCALPHA),i,j,self.visionmap[0,i,j]])


    
    def draw_vision(self, background, color):
        # print(self.surfgrid)
        for i in range(len(self.surfgrid)):
            self.surfgrid[i][0].fill(color)
            self.background.blit(self.surfgrid[i][0],(self.surfgrid[i][1]*ROBOT_WIDTH, self.surfgrid[i][2]*ROBOT_WIDTH, ROBOT_WIDTH, ROBOT_WIDTH))

        background.blit(self.background,(0,0))
        return self.background
            


