import pygame
import math
import numpy as np

from settings import *
from supercover_line import supercover_line

class Robot(pygame.sprite.Sprite):
    def __init__(self, size, world):
        super().__init__()
        #image
        
        self.size = size
        self.image = pygame.Surface([size,size])
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(ROBOT_START_X,ROBOT_START_Y))
        
        #movement
        # self.pos = pygame.math.Vector2(ROBOT_START_X,ROBOT_START_Y)
        self.pos = self.rect.center
        self.speed = SPEED
        self.direction = pygame.math.Vector2(0,0)

        #path
        self.path = []
        self.collision_rects = []
        self.grid = []
        self.viewdist = ROBOT_VISION_LENGTH
        self.fov = ROBOT_FOV

        self.world = world
        

    def get_coord(self):
        col = self.rect.centery // self.size
        row = self.rect.centerx // self.size
        return col,row
    
    def set_path(self, path):
        self.path = path
        self.create_collision_rects()
        self.get_direction()
    
    def create_collision_rects(self):
        if self.path:
            self.collision_rects = []

            for point in self.path:
                x = (point.x *self.size) + (self.size/2)
                y = (point.y *self.size) + (self.size/2)
                rect = pygame.Rect((y-(self.size/4),x-(self.size/4)),((self.size/2),(self.size/2)))
                self.collision_rects.append(rect)
        else:
            self.collision_rects = []

    def get_direction(self):
        if self.collision_rects:
            start = pygame.math.Vector2(self.pos)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            self.direction = (end-start).normalize()
        else:
            self.direction = pygame.math.Vector2(0,0)
            self.path = []
    
    def visionmmap(self, background):
        pxwidth = background.get_width()
        pxheight = background.get_height()

        gridwd = int(pxwidth/self.size)
        gridhi = int(pxheight/self.size) 
        
        self.grid = np.zeros(shape=(gridwd, gridhi))
        # print((gridwd, gridhi))

    def get_vision_grid(self):
        return self.grid

    def check_collisions(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                  del self.collision_rects[0]
                  self.get_direction()

    def vision_check(self):
        for theta in np.arange(0,self.fov,1):
            end_x, end_y = self.viewdist*math.cos(math.radians(theta)),self.viewdist*math.sin(math.radians(theta))
            endp = [(int((end_x) + self.get_coord()[0])), (int((end_y) + self.get_coord()[1]))]
            line = supercover_line(self.get_coord(),endp)
            
            for i in range(len(line)):
                x, y = line[i][1],line[i][0]
                
                if x >= self.grid.shape[0] or y >= self.grid.shape[1] or x<0 or y<0: # disreguard out of range readings
                    continue

                if self.world[x,y] == 0: #if wall is found stop searching the lines
                    self.grid[x,y] = 2
                    break
                else:
                    self.grid[x,y] = 1 
                

    def update(self,background):
        
        self.check_collisions()

        self.vision_check()
        self.drawmap(background)
        

        self.pos += self.direction * self.speed
        self.rect.center = self.pos
    
    def drawmap(self, background):
        map = pygame.Surface((background.get_width(),background.get_height()))
        # print((background.get_width(),background.get_height()))
        # tilemap = []
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.grid[i,j] == 0:
                    # print("grey")
                    color = GREY
                elif self.grid[i,j] == 1:
                    color = WHITE
                elif self.grid[i,j] == 2:
                    color = BLACK 
                # else:
                #     color = WHITE

                # tilemap[i,j] = pygame.Rect(self.width*i ,self.width*j, self.width, self.width)

                # pygame.Rect.update()
                # pygame.surface.blit

                pygame.draw.rect(map, color, (self.size*i, self.size*j, self.size, self.size))
        
        background.blit(map,(0,0))
