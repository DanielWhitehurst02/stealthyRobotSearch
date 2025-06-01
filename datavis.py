import pygame
import matplotlib.pyplot as plt
import pickle

from settings import *
from navgrid import Navgrid
from pathfinder import Pathfinder
from robot import Robot
from observer import Observers

import utils as util

pygame.init()


#create window

background = pygame.image.load(WORLD)
# background = pygame.image.load("worldfile/maze1.png")
backgroundStart = background

# screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen = pygame.display.set_mode((background.get_width(),background.get_height()))

pygame.display.set_caption("Stealthy Robot")
clock = pygame.time.Clock()


background.set_at((0,0), RED) 

#Robot

robwidth = ROBOT_WIDTH
navgrid = Navgrid(robwidth,background,screen)
# navgrid.creategrid()

# grid = creategrid(background,robwidth)

# screen.blit(background,(0,0)) 
# drawgrid( screen, grid, robwidth)
navgrid.loadgrid()
# navgrid.drawgrid(background)
ob_temp = 0
run = False
placing = True
ob_pos = []
pos_temp = []
finished = True


# pathfinder = Pathfinder(navgrid.grid,goal,robwidth)
# robot = Robot(robwidth, navgrid.get_grid(), screen)

print(navgrid.get_grid())

navgrid.drawgrid(screen)

# robot.visionmmap(screen)

with open('office_weightingstealth', 'rb') as inf: 
    path, time_seen, number_time_seen, percent_explored = pickle.load(inf) 
    # print(path) 
    # print(time_seen)
#  navgrid.drawgrid(screen)

pygame.display.update()

while True:

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
   