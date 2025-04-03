#!/usr/bin/env python3
import pygame
import math
import numpy as np


from sys import exit

from settings import *
from navgrid import Navgrid
from pathfinder import Pathfinder

from bresenham import bresenham

pygame.init()


#create window

# background = pygame.image.load("worldfile/conestogo_office.png")
background = pygame.image.load("worldfile/maze1.png")
backgroundStart = background

# screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen = pygame.display.set_mode((background.get_width(),background.get_height()))

pygame.display.set_caption("Stealthy Robot")
clock = pygame.time.Clock()

#Background

# pxarray = pygame.PixelArray(background)
# size = pxarray.shape
# print(size)

# currentcolor = pxarray[0,0]
# print(pxarray[0,0])

# print(white)

# pygame.PixelArray.close(pxarray)


##get pixel color
# print(background.get_at((0,0)))
# print(background.get_at((0,0)) == BLACK)


background.set_at((0,0), RED) 

#Robot

class Robot(pygame.sprite.Sprite):
    def __init__(self, size, pathfinder):
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

    def get_vision(self):
        return self.grid

    def check_collisions(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                  del self.collision_rects[0]
                  self.get_direction()
    
    def update(self):
        
        self.check_collisions()
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

def scan_arc(grid, distance, min, max, rotate, sight_radius, vision_grid,iteration):
    print(robot.get_coord())
    if (distance >= sight_radius or min >= max):
        return 
#  iterate over all integers between min and max  
    for r in range(4):
            
        for i in np.arange(int(distance * min), (distance * max),1):
                if r == 0:
                    xr = distance
                    yr = i
                elif r == 1:
                    xr = i
                    yr = -distance
                elif r == 2:    
                    xr = -distance
                    yr = -i
                elif r == 3:    
                    xr = -i
                    yr = distance
            # # (distance, i) forms an offset from the player representing our current cell.
            # # we rotate it by a multiple of 90 degrees so we can scan in 4 directions
                x = int(robot.get_coord()[1] + xr)
                y = int(robot.get_coord()[0] + yr)
            #     x = robot.get_coord()[1] + xr
            #     y = robot.get_coord()[0] + yr
            # # if our line of sight is blocked,
            # # recursively scan at depth + 1 to the side of the block.
                if x >= grid.shape[0]-1:
                    continue
                elif y >= grid.shape[1]-1:
                    continue
            
                
                
                if grid[x,y] == 0:
                    
                    scan_arc(grid, distance + 1, min, ((i - 0.5) / distance), rotate, sight_radius,vision_grid, iteration+1)
                    min = (i + 0.5) / distance
                    vision_grid[x,y] = 2
                
                else:
                #   // if the current cell is open, we mark it as visible
                    # grid[x,y] = 1
                    vision_grid[x,y] = 1

#   // when we finish scanning a row, continue by scanning the next row
    scan_arc(grid, distance + 1, min, max, rotate, sight_radius, vision_grid, iteration+1)
    

def supercover_line(p0, p1):
    dx = p1[0]-p0[0]
    dy = p1[1]-p0[1]
    nx = abs(dx)
    ny = abs(dy)
    sign_x = 1 if dx > 0 else -1
    sign_y = 1 if dy > 0 else -1

    p = [p0[0], p0[1]]
    points = []
    ix = 0
    iy = 0

    while (ix < nx or iy < ny):

        decision = (1 + 2*ix) * ny - (1 + 2*iy) * nx
        if (decision == 0):
            # next step is diagonal
            p[0] += sign_x
            p[1] += sign_y
            ix += 1
            iy += 1
        elif (decision < 0):
            # next step is horizontal
            p[0] += sign_x
            ix += 1
        else:
            # next step is vertical
            p[1] += sign_y
            iy += 1

        points.append((p[0],p[1]))
    return points

# class Visiongrid:
#    def __init__(self, background: pygame.Surface, robot, map: Navgrid):
#     self.robot = robot
#     self.map = map.get_grid()
#     self.background = background

#     self.sight_grid = np.zeros(shape=(self.map.shape))

#    def drawmap(self, surface):
#     surface.blit(self.sight_grid,(0,0))
 




robwidth: int = 5

navgrid = Navgrid(robwidth,background,screen)

navgrid.creategrid()

# grid = creategrid(background,robwidth)

goal = (400,500)



screen.blit(background,(0,0))
# drawgrid( screen, grid, robwidth)
navgrid.loadgrid()
# navgrid.drawgrid(background)

pathfinder = Pathfinder(navgrid.grid,goal,robwidth)
robot = Robot(robwidth, pathfinder)

robot.visionmmap(background)

print(navgrid.get_grid().shape)
# scan_arc(navgrid.get_grid(),0,-1,1,0,10,robot.get_vision(),0)

linedist = 30

# for theta in range(0,360,1):
#     end_x, end_y = linedist*math.cos(math.radians(theta)),linedist*math.sin(math.radians(theta))

#     line = list(bresenham(robot.get_coord()[0], robot.get_coord()[1], int(end_x), int(end_y)))
#             #    for i in range(navgrid.grid.shape[0]):
#             #        for j in range(navgrid.grid.shape[1]):
#             #            for k in range(len(line)):
#             #             if line[k] == [i,j]:
#     for i in range(len(line)):
#         pygame.draw.rect(background, RED_TRANS, (robwidth*line[i][1], robwidth*line[i][0], robwidth, robwidth))


pygame.display.update()

# line = supercover_line(robot.get_coord(),[10,10])
# print (line)

# for i in range(len(line)):
#     pygame.draw.rect(background, RED_TRANS, (robwidth*line[i][1], robwidth*line[i][0], robwidth, robwidth))

while True:
    
    # linemap = pygame.Surface((background.get_width(),background.get_height()))
    
    # scan_arc(navgrid.get_grid(),0,-1,1,0,10,robot.get_vision(),0)
    
    # navgrid.drawgrid(background)
    linemap = []

    for theta in np.arange(0,360,1):
        end_x, end_y = linedist*math.cos(math.radians(theta)),linedist*math.sin(math.radians(theta))
        # print (int(end_x - robot.get_coord()[0]),int(end_y - robot.get_coord()[1]))
        endp = [(int((end_x) + robot.get_coord()[0])), (int((end_y) + robot.get_coord()[1]))]
        # line = list(bresenham(robot.get_coord()[0], robot.get_coord()[1], (int((end_x) + robot.get_coord()[0])), (int((end_y) + robot.get_coord()[1]))))
        line = supercover_line(robot.get_coord(),endp)
                #    for i in range(navgrid.grid.shape[0]):
                #        for j in range(navgrid.grid.shape[1]):
                #            for k in range(len(line)):
                #             if line[k] == [i,j]:
        # print(line)
        for i in range(len(line)):
            pygame.draw.rect(background, GREEN, (robwidth*line[i][1], robwidth*line[i][0], robwidth, robwidth))

    theta = 0

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
           pathfinder.create_path(robot.get_coord())

           robot.set_path(pathfinder.path)

           mouse_pos = pygame.mouse.get_pos()
           end_x,end_y = int(mouse_pos[1]/robwidth),int(mouse_pos[0]/robwidth)
           linemap = pygame.Surface((background.get_width(),background.get_height()))

           line = []
           line = list(bresenham(robot.get_coord()[0], robot.get_coord()[1], end_x, end_y))
        #    for i in range(navgrid.grid.shape[0]):
        #        for j in range(navgrid.grid.shape[1]):
        #            for k in range(len(line)):
        #             if line[k] == [i,j]:
           for i in range(len(line)):
            pygame.draw.rect(background, RED_TRANS, (robwidth*line[i][1], robwidth*line[i][0], robwidth, robwidth))
  
        #    print(line[1][0])
    
    # screen.fill(white)
    screen.blit(background,(0,0))
    robot.drawmap(background)
    # navgrid.drawgrid(background)
    
    # screen.blit()
    
    pathfinder.update(screen)
    robot.update()
    screen.blit(robot.image,robot.pos)
    # if linemap:
    #     screen.blit(background,(0,0))



    pygame.display.update()
    clock.tick(FPS)
    