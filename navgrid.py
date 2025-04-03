import pygame
import math
import numpy as np

from settings import *


class Navgrid:

  def __init__(self,width, background: pygame.Surface, screen):
      self.width = width
      self.background = background
      self.screen = screen
      self.map = pygame.Surface((background.get_width(),background.get_height()))

  def creategrid(self):
      pxwidth = self.background.get_width()
      pxheight = self.background.get_height()

      # print(pxwidth)
      # print(pxheight)

      gridwd = int(pxwidth/self.width)
      gridhi = int(pxheight/self.width) 
      
      grid = np.zeros(shape=(gridwd, gridhi))

      # print(grid.shape)
      # print(gridwd, gridhi)

      for i in range(gridwd):
        # print(i)
        for j in range(gridhi):
          grid[i,j] = 1
          for k in range(self.width):
            for l in range(self.width):
              # background.get_at((i+k,j+l))
              if self.background.get_at(((i*self.width)+k,(j*self.width)+l)) == BLACK:
                grid[i,j] = 0
                break
              
          else:
            continue  # if a black pixel is found go to next grid spot
          break

      # print(grid)
      self.grid = grid

  # def updategrid(self, line):
  #   self.grid = 


  def loadgrid(self):
    # tilemap = []
    for i in range(self.grid.shape[0]):
      for j in range(self.grid.shape[1]):
        if self.grid[i,j] == 1:
          color = WHITE
        elif self.grid[i,j] == 0:
          color = BLACK
        elif self.grid[i,j] == 2:
          color = GREY 
        else:
          color = WHITE

        # tilemap[i,j] = pygame.Rect(self.width*i ,self.width*j, self.width, self.width)

        # pygame.Rect.update()
        # pygame.surface.blit

        pygame.draw.rect(self.map, color, (self.width*i, self.width*j, self.width, self.width))
  
  def get_grid(self):
    return self.grid
  
  def drawgrid(self, surface):
     surface.blit(self.map,(0,0))