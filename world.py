#!/usr/bin/env python3
import pygame
import math
import numpy as np


from sys import exit

from settings import *
from navgrid import Navgrid
from pathfinder import Pathfinder
from robot import Robot

# from bresenham import bresenham

pygame.init()


#create window

background = pygame.image.load(WORLD)
# background = pygame.image.load("worldfile/maze1.png")
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
robot = Robot(robwidth, navgrid.get_grid())

robot.visionmmap(background)

print(navgrid.get_grid().shape)
# scan_arc(navgrid.get_grid(),0,-1,1,0,10,robot.get_vision(),0)

# linedist = 30


pygame.display.update()

while True:
    
    # linemap = pygame.Surface((background.get_width(),background.get_height()))
    
    # scan_arc(navgrid.get_grid(),0,-1,1,0,10,robot.get_vision(),0)
    
    # navgrid.drawgrid(background)
    linemap = []

    # for theta in np.arange(0,360,1):
    #     end_x, end_y = linedist*math.cos(math.radians(theta)),linedist*math.sin(math.radians(theta))
    #     # print (int(end_x - robot.get_coord()[0]),int(end_y - robot.get_coord()[1]))
    #     endp = [(int((end_x) + robot.get_coord()[0])), (int((end_y) + robot.get_coord()[1]))]
    #     # line = list(bresenham(robot.get_coord()[0], robot.get_coord()[1], (int((end_x) + robot.get_coord()[0])), (int((end_y) + robot.get_coord()[1]))))
    #     line = supercover_line(robot.get_coord(),endp)
    #             #    for i in range(navgrid.grid.shape[0]):
    #             #        for j in range(navgrid.grid.shape[1]):
    #             #            for k in range(len(line)):
    #             #             if line[k] == [i,j]:
    #     # print(line)
    #     for i in range(len(line)):
    #         pygame.draw.rect(background, GREEN, (robwidth*line[i][1], robwidth*line[i][0], robwidth, robwidth))

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
  
        #    print(line[1][0])
    # robot.vision_check()
    # screen.fill(white)
    screen.blit(background,(0,0))
    # robot.drawmap(background)
    # navgrid.drawgrid(background)
    
    # screen.blit()
    robot.update(background)
    pathfinder.update(screen)
   
    screen.blit(robot.image,robot.pos)
    # if linemap:
    #     screen.blit(background,(0,0))



    pygame.display.update()
    clock.tick(FPS)
    