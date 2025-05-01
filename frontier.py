import pygame
import math
import numpy as np

from settings import *

#need visited cells calculated

class Frontier:
    def __init__(self, map):
        self.map = map
        self.frontiers = []
        self.new_space = []

    def map_update(self, map):
        self.map = map
    
    def get_frontiers(self):
        # for i in range(len(self.new_space)): #[Cell info, x, y]
        # self.frontiers = []
        threshold = 0 
        for i in range(self.map.shape[0]): #[Cell info, x, y]
            for j in range(self.map.shape[1]):
                if self.map[i,j] == 1:   #check if the cell is empty space
                    # x, y = self.new_space[i][1],self.new_space[i][2]
                    threshold = 0
                    for k in range(-1,2,1):
                        if i<0 or j<0: # disreguard out of range readings
                            break
                        for l in range(-1, 2,1):
                            if i+k >= self.map.shape[0] or j+l >= self.map.shape[1] or i<0 or j<0: # disreguard out of range readings
                                break
                            if self.map[i+k,j+l] == 0:
                                threshold += 1
                    # print(threshold)
                    if threshold >= FRONT_THRESHOLD:
                        self.frontiers.append([i,j])
                        # if (self.map[i+k,j] == 0 or self.map[i,j+k] == 0 ) and i != 0:    #if adjacent cells are unknown add frontier
                        #     self.frontiers.append([i,j])
                        #     break

                              
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
