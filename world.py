#!/usr/bin/env python3
import pygame
import math
import numpy as np
import pickle


from sys import exit

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
finished = False

data_name = 'office_weightingstealth'


# pathfinder = Pathfinder(navgrid.grid,goal,robwidth)
# robot = Robot(robwidth, navgrid.get_grid(), screen)

print(navgrid.get_grid())

navgrid.drawgrid(screen)

# robot.visionmmap(screen)

pygame.display.update()

while True:
    
    while run == False:
        
        navgrid.drawgrid(screen)
        util.draw_active_cell(navgrid.get_grid(),screen)
        # pygame.draw.rect(screen, BLUE, [200*ROBOT_WIDTH,200*ROBOT_WIDTH ,ROBOT_WIDTH,ROBOT_WIDTH])

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                mouse_pos = pygame.mouse.get_pos()
                pos_x,pos_y = int(mouse_pos[1]/robwidth),int(mouse_pos[0]/robwidth)
                
                if placing:
                    pos_temp = [pos_x,pos_y]
                    placing = False
                else:
                    angle = util.getAngle(pos_temp,[pos_x,pos_y])
                    ob_pos.append([pos_temp[0],pos_temp[1],angle-45])
                    placing = True

                # ob_pos.append([pos_temp[0],pos_temp[1],90])
                ## office
                # ob_pos = [[1, 27, 7.253194612725338], [33, 1, 15.255118703057782], [33, 122, -77.27564431457763]]

                ## Warehouse1
                # ob_pos = [[29, 4, -45.0], [50, 73, -45.0], [66, 15, -45.0]]
                # util.drawtriangle(screen,mouse_pos,YELLOW)


                #Place observers
                if ob_temp == (OB_NUMBER):
                    print(ob_pos)
                    observer = Observers(navgrid.get_grid(),360,ob_pos,PURPLE,screen)
                    vision = observer.vision()
                    robot = Robot(robwidth, observer.add_observers_tomap(navgrid.get_grid()), screen,ob_pos,vision)
                    robot.visionmmap(screen)
                    
                    observer.def_vision_map()
                    observer.draw_vision(screen,YELLOW_TRANS)

                    run = True
                else:
                    if placing == True:
                        ob_temp += 1
        pygame.display.flip()


    if run and not finished:


        linemap = []

        

        theta = 0

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #    pathfinder.create_path(robot.get_coord())

            #    robot.set_path(pathfinder.path)

            #    mouse_pos = pygame.mouse.get_pos()
            #    end_x,end_y = int(mouse_pos[1]/robwidth),int(mouse_pos[0]/robwidth)
            #    linemap = pygame.Surface((background.get_width(),background.get_height()))
                

    
            #    print(line[1][0])
        # robot.vision_check()

        
        # screen.blit()
        # vision_back = observer.draw_vision(screen,YELLOW_TRANS)

        # navgrid.drawgrid_extra(screen,vision_back)
        
        finish = robot.update(screen)

        # observer.draw_vision(screen,YELLOW_TRANS)


        # screen.fill(white)
        # screen.blit(background,(0,0))
        # robot.drawmap(background)

        # pathfinder.update(screen)
    
        screen.blit(robot.image,robot.rect.center)

        # #testing transparency
        # shape_surf = pygame.Surface(pygame.Rect(0, 0, 255, 127).size, pygame.SRCALPHA)
        # # pygame.draw.rect(shape_surf, (55, 90, 140, 140), shape_surf.get_rect())
        # shape_surf.fill((55, 90, 140, 140))
        # screen.blit(shape_surf, (0, 0, 255, 127) )
        # shape_surf.fill((128,0,0,128))
        # screen.blit(shape_surf, (0, 0, 255, 127) )

        if finish:
            print("environment explored, plotting results")
            finished = True
            # print(robot.get_path())
            path, time_seen, number_time_seen, percent_explored = robot.get_eval()

            with open(data_name,"wb") as outf:
                pickle.dump([path, time_seen, number_time_seen, percent_explored],outf)
            pygame.quit()
            exit()





    # print(clock.get_time())
    pygame.display.flip()
    clock.tick(FPS)
