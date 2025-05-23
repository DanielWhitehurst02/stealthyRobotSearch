import pygame
import math
import numpy as np

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

from settings import *


class Pathfinder:
  def __init__(self,matrix,width):
    #setup
    self.matrix = matrix
    self.grid = Grid(matrix= matrix)
    self.goal = []
    self.width = width
    self.select_surf = pygame.image.load('select.png').convert_alpha()
    self.select_surf = pygame.transform.scale(self.select_surf,(width,width))
    # self.select_surf.fill(GREEN)
    self.path = []
   

  def updateGoal(self,goal):
    self.goal = goal

  def updateMap(self,matrix):
    # matrix_temp = np.zeros(shape=(matrix.shape[0],matrix.shape[1]))
    self.matrix = np.zeros(shape=(matrix.shape[0],matrix.shape[1]))
    
    for i in range(matrix.shape[0]):
      for j in range(matrix.shape[1]):
        if matrix[i,j] == 1:
          self.matrix[i,j] = 1
        else:
          self.matrix[i,j] = 0
      
    # self.matrix[5,5] = 1

    # self.matrix = matrix
    self.grid = Grid(matrix= self.matrix)

  def draw_active_cell(self, screen):
    mouse_pos = pygame.mouse.get_pos()
  
    row = int(mouse_pos[0]/self.width)
    col = int(mouse_pos[1]/self.width)
  #  print(row, col)

    if (0 <= row) and (row < self.matrix.shape[0]) and (0 <= col) and (col < (self.matrix.shape[1])) :
      current_cell_value = self.matrix[row][col]
      if current_cell_value == 1:
        rect = pygame.Rect((row*self.width,col*self.width),(self.width,self.width))
        screen.blit(self.select_surf,rect)
        
  def create_path(self,start,goal):
    #start
    start_x, start_y = int(start[0]), int(start[1])
    start = self.grid.node(start_x,start_y) 
    
    end_x, end_y = int(goal[1]),int(goal[0])
    # print("Start: "+ str(start_x) + " " + str(start_y) + " End: " + str(end_x) +' '+ str(end_y))
    # #end
    # mouse_pos = pygame.mouse.get_pos()
    # end_x,end_y = int(mouse_pos[1]/self.width),int(mouse_pos[0]/self.width)
    end = self.grid.node(end_x, end_y)

    ##seeing diagonals between walls as ok to move through

    #path
    finder = AStarFinder(diagonal_movement= DiagonalMovement.always)
    # print(self.grid.grid_str())
    # print(self.matrix)
    self.path, _ = finder.find_path(start,end,self.grid)
    # print(self.path)

    return self.path
  
  def draw_path(self, screen):
     if self.path:
        points = []
        for point in self.path:
          x = (point.x * self.width) + (self.width/2)
          y = (point.y * self.width) + (self.width/2)
          # x = point[0] * self.width
          # y = point[1] * self.width
          points.append((y,x))

          if len(points) >= 2:
            pygame.draw.lines(screen,GREEN,False,points,5)

  def update(self, screen):
    # self.draw_active_cell(screen)
    self.draw_path(screen)
    

