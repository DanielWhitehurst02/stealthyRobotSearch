#!/usr/bin/env python3
import pygame
import math
import numpy as np


from sys import exit

from settings import *
from navgrid import Navgrid
from pathfinder import Pathfinder

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
print(background.get_at((0,0)))
print(background.get_at((0,0)) == BLACK)


background.set_at((0,0), RED) 

#Robot

class Robot(pygame.sprite.Sprite):
    def __init__(self, size):
        super().__init__()
        self.image = pygame.Surface([size,size])
        self.image.fill(RED)
        self.pos = pygame.math.Vector2(ROBOT_START_X,ROBOT_START_Y)



robwidth: int = 10

robot = Robot(robwidth)

navgrid = Navgrid(robwidth,background,screen)

navgrid.creategrid()

# grid = creategrid(background,robwidth)

goal = (400,500)



screen.blit(background,(0,0))
# drawgrid( screen, grid, robwidth)
navgrid.loadgrid()
navgrid.drawgrid(background)

pathfinder = Pathfinder(navgrid.grid,goal,robwidth)


pygame.display.update()

while True:


    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
           pathfinder.create_path()
    # screen.fill(white)
    screen.blit(background,(0,0))

    navgrid.drawgrid(background)
    # screen.blit()
    screen.blit(robot.image,robot.pos)
    pathfinder.update(screen)

    pygame.display.update()
    clock.tick(FPS)
    