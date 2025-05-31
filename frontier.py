import pygame
import math
import numpy as np
import utils as util

from settings import *


#need visited cells calculated

##TODO calculate the vision cost of a frontier
##TODO calculate info gain from frontier

class Frontier:
    def __init__(self, map):
        self.map = map
        self.frontiers = []
        self.new_space = []
        self.frontiersqueue = []

    def map_update(self, map, vision):
        self.map = map
        self.new_space = vision

    def frontier_check(self,i,j, wall_thres):
        threshold = 0
        wall_threshold = 0
        frontier = False
    
        for k in range(-1,2,1):            
            if i<0 or j<0: # disreguard out of range readings
                continue
            for l in range(-1, 2,1): ## check surrounding tiles
                # print("K, l: " +str(k) + " , " + str(l))
                if i+k >= self.map.shape[0] or j+l >= self.map.shape[1] or i<0 or j<0: # disreguard out of range readings
                    continue
                map_val = self.map[i+k,j+l]
                if map_val == 0:  ## if there is adjacent unknown spaces increment
                    threshold += 1
                elif map_val == 2:
                    wall_threshold += 1

        # print(wall_threshold)
        if threshold >= FRONT_THRESHOLD and wall_threshold < wall_thres:
            frontier = True


        return frontier

    def queue_process(self):
        grouped = util.group_adjacents(self.frontiersqueue)
        # print("grouped points")
        # print(grouped)
        for i in range(len(grouped)):
            # print(i)
            sum_x,sum_y = 0,0
            num_points = len(grouped[i])
            for j in range(len(grouped[i])):
                sum_x += grouped[i][j][0]
                sum_y += grouped[i][j][1]
            
            midpoint = [int(sum_x/num_points),int(sum_y/num_points)]
            self.frontiers.append(midpoint)
            #### TODO gives values inside walls, pathfinder wont go there at all

    
    def get_frontiers(self,threshold):
        # for i in range(len(self.new_space)): #[Cell info, x, y]
        self.frontiers = []
        # temp_map = self.map
        # self.frontiersqueue = []

        # index = 0

        for i in range(len(self.new_space)):
            if self.new_space[i][0] == 1:
                x,y = self.new_space[i][1], self.new_space[i][2]
                # index += 1

                self.frontier_check(x,y,threshold)

            self.queue_process()


        if not self.frontiers:

            # index = 0
            for i in range(self.map.shape[0]): #[Cell info, x, y]
                for j in range(self.map.shape[1]):
                    
                    if self.map[i,j] == 1:   #check if the cell is empty space
                        if self.frontier_check(i,j,threshold):
                            self.frontiersqueue.append([i,j])
                        

                    # elif self.map[i,j] ==5:
                    #     print("tile already checked: " + str(i) + " , " + str(j))
            # print("frontiers queue: " + str(self.frontiersqueue))
            self.queue_process()
            # print( "frontiers: "+str(self.frontiers))



        # print(self.frontiers)
            
                              
        return self.frontiers
    
    def get_frontiers_active(self, vision): #### gets stuck when current reading has no unknown tiles
        self.frontiers = []
        for i in range(len(vision)):
            if vision[i][0] == 1:
                x,y = vision[i][1], vision[i][2]
                threshold = 0
                for k in range(-1,2,1):
                    if y<0 or x<0: # disreguard out of range readings
                        break
                    for l in range(-1, 2,1):
                        if (x+k or y+l) < 0:
                            print("reading wrapped")
                            break

                        if x+k >= self.map.shape[0] or y+l >= self.map.shape[1] or x<0 or y<0: # disreguard out of range readings
                            break
                        if self.map[x+k,y+l] == 0:
                            threshold += 1
                # print(threshold)
                if threshold >= FRONT_THRESHOLD:
                    self.frontiers.append([x,y])

        return self.frontiers
    
    def pick_frontier(self):
        goal = []
        return goal
    
    # def frontier_vis(self, background):
    #     color = BLUE
    #     for i in range(len(self.frontiers)): #[Cell info, x, y]
    #         pygame.draw.rect(background, color, self.frontiers[i][0],self.frontiers[i][1])
