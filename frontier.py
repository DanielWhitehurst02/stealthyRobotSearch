import pygame
import math
import numpy as np
import utils as util

from settings import *


#need visited cells calculated

class Frontier:
    def __init__(self, map):
        self.map = map
        self.frontiers = []
        self.new_space = []
        self.frontiersqueue = []

    def map_update(self, map, vision):
        self.map = map
        self.new_space = vision

    def frontier_check(self,i,j):
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
        if threshold >= FRONT_THRESHOLD and wall_threshold < 4:
            frontier = True


        return frontier
    

    
    # def frontier_check(self,i,j,index):
    #     threshold = 0
    #     adjacent_space = []
    #     self.map[i,j] = 5 
    #     for k in range(-1,2,1):
            
    #         if i<0 or j<0: # disreguard out of range readings
    #             continue
    #         for l in range(-1, 2,1): ## check surrounding tiles
    #             # print("K, l: " +str(k) + " , " + str(l))
    #             if i+k >= self.map.shape[0] or j+l >= self.map.shape[1] or i<0 or j<0: # disreguard out of range readings
    #                 continue
    #             map_val = self.map[i+k,j+l]
    #             if map_val == 0:  ## if there is adjacent unknown spaces increment
    #                 threshold += 1
    #             if map_val == 1:
    #                 adjacent_space.append([i+k,j+l])
    #                 # self.map[i+k,j+l] = 5 ## set tile as checked
                    
    #     if threshold >= FRONT_THRESHOLD:     ## if it is a frontier tile
    #         # threshold = 0
    #         self.frontiersqueue.append([i,j, index])  # add to frontier queue
    #         # print(self.frontiersqueue)
    #         # print("I, J: " + str(i) + " , " + str(j) +" len: " + str(self.map.shape))
    #         for o in range(len(adjacent_space)):
    #             print(o)
    #             k,l = adjacent_space[o]
    #             self.frontier_check(i+k,j+l,index)
    #             # self.map[k,l] = 5 ## set tile as checked
                
            

    #         if i >= self.map.shape[0] or j >= self.map.shape[1] or i<0 or j<0: # disreguard out of range readings
    #             # break
    #             return True
    #         # self.map[i,j] = 5 ## set tile as checked
    #         # print(adjacent_space)

    #         return True
        
        
            # break

    # def adjacent_check(self,i,j,index):
    #     threshold = 0
    #     for k in range(-1,2,1): 
    #         if i<0 or j<0: # disreguard out of range readings
    #             break
    #         for l in range(-1, 2,1): ## check surrounding tiles
    #             if i+k >= self.map.shape[0] or j+l >= self.map.shape[1] or i<0 or j<0: # disreguard out of range readings
    #                 break
    #             if self.map[i+k,j+l] == 0:  ## if there is adjacent unknown spaces increment
    #                 threshold += 1
                
    #         if threshold >= FRONT_THRESHOLD:     ## if it is a frontier tile
    #             # threshold = 0
    #             self.frontiersqueue.append([i,j, index])  # add to frontier queue
    #             # print("I, J: " + str(i) + " , " + str(j) +" len: " + str(self.map.shape))
    #             if i >= self.map.shape[0] or j >= self.map.shape[1] or i<0 or j<0: # disreguard out of range readings
    #                 break
    #             self.map[i,j] = 5 ## set tile as checked
    #             # self.adjacent_check(i+k,j+l,index)
    #             break

    # def adjacent_check_vision(self,i,x,y,index):
    #     threshold = 0
    #     for k in range(-1,2,1):
    #         if x<0 or y<0: # disreguard out of range readings
    #             break
    #         for l in range(-1, 2,1): ## check surrounding tiles
    #             if x+k >= self.map.shape[0] or y+l >= self.map.shape[1] or x<0 or y<0: # disreguard out of range readings
    #                 break
    #             if self.map[x+k,y+l] == 0:
    #                 threshold += 1
                
    #         if threshold >= FRONT_THRESHOLD:
    #             # threshold = 0
    #             self.frontiersqueue.append([x,y, index])
    #             # print("I, J: " + str(i) + " , " + str(j) +" len: " + str(self.map.shape))
    #             if x >= self.map.shape[0] or y >= self.map.shape[1] or x<0 or y<0: # disreguard out of range readings
    #                 break
    #             self.new_space[i][0] = 5
    #             self.adjacent_check(x+k,y+l,index)
    #             break
                    
    #     # return map
    
    # def queue_process(self,index):
    #     search = True
    #     o = 0
    #     # print(self.frontiersqueue)
    #     while search:
    #         # print(self.frontiersqueue)
    #         if self.frontiersqueue:
    #             index = self.frontiersqueue[o][2]
    #             # self.frontiers.append([self.frontiersqueue[o][0],self.frontiersqueue[o][1]])
    #             self.frontiers.append(self.frontiersqueue[o])
    #             # print(self.frontiers)

    #             num_cells = 0

    #             for p in range(len(self.frontiersqueue)):   ## get the number of items in the list with the same index
    #                 new_index = self.frontiersqueue[p][2]
    #                 if new_index == index:
    #                     num_cells += 1

    #             check_num = 0
    #             # print(num_cells)

    #             while num_cells > 0:
    #                 new_index = self.frontiersqueue[check_num][2]
    #                 if new_index == index:
    #                     num_cells += -1
    #                     del self.frontiersqueue[check_num]


    #                     # print(" numcells: " + str(num_cells) + " checknum: " + str(check_num))
    #                     # print(self.frontiersqueue)
    #                 else:
    #                     check_num += 1
    #             # print(self.frontiers)
                
    #         else:
    #             search = False

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

    
    def get_frontiers(self):
        # for i in range(len(self.new_space)): #[Cell info, x, y]
        self.frontiers = []
        # temp_map = self.map
        # self.frontiersqueue = []

        index = 0

        for i in range(len(self.new_space)):
            if self.new_space[i][0] == 1:
                x,y = self.new_space[i][1], self.new_space[i][2]
                index += 1

                self.frontier_check(x,y)

            self.queue_process()


        if not self.frontiers:

            index = 0
            for i in range(self.map.shape[0]): #[Cell info, x, y]
                for j in range(self.map.shape[1]):
                    
                    if self.map[i,j] == 1:   #check if the cell is empty space
                        # index += 1
                        if self.frontier_check(i,j):
                            self.frontiersqueue.append([i,j])
                        # self.adjacent_check(i,j, index)
                        # front = self.frontier_check(i,j,index)
                        # if front:
                        #     index +=1
                        

                    # elif self.map[i,j] ==5:
                    #     print("tile already checked: " + str(i) + " , " + str(j))
            # print("frontiers queue: " + str(self.frontiersqueue))
            self.queue_process()
            print( "frontiers: "+str(self.frontiers))
                    # search = True
                    # o = 0
                    # while search:
                    #     if self.frontiersqueue:
                    #         index = self.frontiersqueue[o][2]
                    #         self.frontiers.append([self.frontiersqueue[o][0],self.frontiersqueue[o][1]])

                    #         num_cells = 0

                    #         for p in range(len(self.frontiersqueue)):   ## get the number of items in the list with the same index
                    #             new_index = self.frontiersqueue[p][2]
                    #             if new_index == index:
                    #                 num_cells += 1

                    #         check_num = 0

                    #         while num_cells > 0:
                    #             new_index = self.frontiersqueue[check_num][2]
                    #             if new_index == index:
                    #                 num_cells += -1
                    #                 del self.frontiersqueue[check_num]
                    #             else:
                    #                 check_num += 1
                    #     else:
                    #         search = False

                    # o += 1
                            # if (self.map[i+k,j] == 0 or self.map[i,j+k] == 0 ) and i != 0:    #if adjacent cells are unknown add frontier
                            #     self.frontiers.append([i,j])
                            #     break



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
