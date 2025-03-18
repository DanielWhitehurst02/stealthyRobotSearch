#!/usr/bin/env python3
import pygame
import math
import numpy as np

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

from sys import exit

from settings import *
from navgrid import Navgrid

pygame.init()


#create window

background = pygame.image.load("worldfile/conestogo_office.png")
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
print(background.get_at((0,0)))
print(background.get_at((0,0)) == BLACK)


background.set_at((0,0), RED) 


       
class Pathfinder:
  def __init__(self,matrix,goal,width):
    #setup
    self.matrix = matrix
    self.grid = Grid(matrix= matrix)
    self.goal = goal
    self.width = width
    self.select_surf = pygame.image.load('select.png').convert_alpha()
    self.select_surf = pygame.transform.scale(self.select_surf,(width,width))
    # self.select_surf.fill(GREEN)

  def updateGoal(self,goal):
    self.goal = goal

  def draw_active_cell(self):
    mouse_pos = pygame.mouse.get_pos()
  
    row = int(mouse_pos[0]/self.width)
    col = int(mouse_pos[1]/self.width)
  #  print(row, col)
    current_cell_value = self.matrix[row][col]
    if current_cell_value == 0:
      rect = pygame.Rect((row*self.width,col*self.width),(self.width,self.width))
      screen.blit(self.select_surf,rect)

  def update(self):
    self.draw_active_cell()




#Robot

class Robot(pygame.sprite.Sprite):
    def __init__(self, size):
        super().__init__()
        self.image = pygame.Surface([size,size])
        self.image.fill(RED)
        self.pos = pygame.math.Vector2(ROBOT_START_X,ROBOT_START_Y)



robwidth: int = 5

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
# goal = [32,24]

# pygame.draw.rect(screen, c, (width*i, width*j, width, width))

pygame.display.update()

while True:
    
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # screen.fill(white)
    screen.blit(background,(0,0))

    navgrid.drawgrid(background)
    # screen.blit()
    screen.blit(robot.image,robot.pos)
    pathfinder.draw_active_cell()

    pygame.display.update()
    clock.tick(FPS)
    