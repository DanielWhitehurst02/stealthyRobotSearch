#!/usr/bin/env python3
import pygame
import math
import numpy as np
from pathfinding.core.grid import Grid

from sys import exit
from settings import *

pygame.init()

#colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
#create window

# background = pygame.image.load("worldfile/simpleenv.png")
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

def creategrid(background: pygame.Surface, width):
    pxwidth = background.get_width()
    pxheight = background.get_height()

    # print(pxwidth)
    # print(pxheight)

    gridwd = int(pxwidth/robwidth)
    gridhi = int(pxheight/robwidth) 
    
    grid = np.zeros(shape=(gridwd, gridhi))

    print(grid.shape)
    print(gridwd, gridhi)

    for i in range(gridwd):
      # print(i)
      for j in range(gridhi):
        #0
        for k in range(robwidth):
          for l in range(robwidth):
            # background.get_at((i+k,j+l))
            if background.get_at(((i*robwidth)+k,(j*robwidth)+l)) == BLACK:
              grid[i,j] = 1
              break
        else:
          continue  # only executed if the inner loop did NOT break
        break

    # print(grid)
    return grid
def drawgrid( win, grid, width):

  for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
      if grid[i,j] == 0:
        color = WHITE
      elif grid[i,j] == 1:
        color = BLACK 
      else:
        color = WHITE

      pygame.draw.rect(win, color, (width*i, width*j, width, width))

       




#Robot

class Robot(pygame.sprite.Sprite):
    def __init__(self, size):
        super().__init__()
        self.image = pygame.Surface([size,size])
        self.image.fill(RED)
        self.pos = pygame.math.Vector2(ROBOT_START_X,ROBOT_START_Y)



robwidth: int = 10

robot = Robot(robwidth)
grid = creategrid(background,robwidth)
screen.blit(background,(0,0))
drawgrid( screen, grid, robwidth)

goal = [32,24]

# pygame.draw.rect(screen, c, (width*i, width*j, width, width))

pygame.display.update()

while True:
    
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # screen.fill(white)

    

    screen.blit(robot.image,robot.pos)


    pygame.display.update()
    clock.tick(FPS)
    