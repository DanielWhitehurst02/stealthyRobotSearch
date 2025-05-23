import pygame
import math
import numpy as np

from settings import *
from supercover_line import supercover_line
from frontier import Frontier
from pathfinder import Pathfinder

class Robot(pygame.sprite.Sprite):
    def __init__(self, size, world, background, observer_pos, observers_vision_map):
        super().__init__()
        #image
        
        self.size = size
        self.image = pygame.Surface([size,size])
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(ROBOT_START_X,ROBOT_START_Y))
        
        #movement
        # self.pos = pygame.math.Vector2(ROBOT_START_X,ROBOT_START_Y)
        self.pos = self.rect.center
        self.speed = SPEED
        self.direction = pygame.math.Vector2(0,0)

        #path
        self.path = []
        self.collision_rects = []
        self.grid = []
        self.viewdist = ROBOT_VISION_LENGTH
        self.fov = ROBOT_FOV

        self.world = world

        self.map = pygame.Surface((background.get_width(),background.get_height()),pygame.SRCALPHA)

        self.k = 0

        self.frontier = Frontier(self.grid)
        self.pathfinder = Pathfinder(self.grid,size)

        self.goal = False
        self.goalnum = 0
        
        self.observer_pos = observer_pos
        self.observers_known = []
        self.observers_vision = observers_vision_map


    def get_coord(self):
        col = self.rect.centery // self.size
        row = self.rect.centerx // self.size
        return col,row
    
    def set_path(self, path):
        self.path = path
        self.create_collision_rects()
        self.get_direction()
        
    def set_observervision(self, observers_vision_map):
        self.observers_vision = observers_vision_map
    
    def create_collision_rects(self):
        if self.path:
            self.collision_rects = []

            for point in self.path:
                x = (point.x *self.size) + (self.size/2)
                y = (point.y *self.size) + (self.size/2)
                rect = pygame.Rect((y-(self.size/4),x-(self.size/4)),((self.size/2),(self.size/2)))
                self.collision_rects.append(rect)
        else:
            self.collision_rects = []
            print("no collision rects")

    def get_direction(self):
        if self.collision_rects:
            start = pygame.math.Vector2(self.pos)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            # print(str(start) + " to End " +str(end))
            if ((end[0]-start[0]) == 0) and ((end[1]-start[1]) == 0):
                self.direction = pygame.math.Vector2(0,0)
                self.path = []
                return
            else:
                self.direction = (end-start).normalize()
        else:
            self.direction = pygame.math.Vector2(0,0)
            self.path = []

            print(self.direction)
    
    def visionmmap(self, background):
        pxwidth = background.get_width()
        pxheight = background.get_height()

        gridwd = int(pxwidth/self.size)
        gridhi = int(pxheight/self.size) 
        
        self.grid = np.zeros(shape=(gridwd, gridhi))
        # self.gridnew = np.zeros(shape=(gridwd, gridhi))
        self.gridnew = []
        self.gridbuffer = []
        # print((gridwd, gridhi))
        

        self.surfgrid = np.zeros(shape=(gridwd, gridhi),dtype=(pygame.Surface), order="F")
        
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                color = GREY
                self.surfgrid[i,j] = pygame.Surface(pygame.Rect((self.size*i, self.size*j, self.size, self.size)).size, pygame.SRCALPHA)
                self.surfgrid[i,j].fill((color))
                self.map.blit(self.surfgrid[i,j], (self.size*i, self.size*j, self.size, self.size))
        
        background.blit(self.map,(0,0))

    def get_vision_grid(self):
        return self.grid

    def check_collisions(self):
        if self.collision_rects:
            
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                #   print("real")
                  del self.collision_rects[0]
                  self.get_direction()

    def vision_check(self):

        self.gridnew.clear()
        for theta in np.arange(0,self.fov,1):
            end_x, end_y = self.viewdist*math.cos(math.radians(theta)),self.viewdist*math.sin(math.radians(theta))
            endp = [(int((end_x) + self.get_coord()[0])), (int((end_y) + self.get_coord()[1]))]
            line = supercover_line(self.get_coord(),endp)
            
            for i in range(len(line)):
                x, y = line[i][1],line[i][0]
                
                if x >= self.grid.shape[0] or y >= self.grid.shape[1] or x<0 or y<0: # disreguard out of range readings
                    continue

                if self.world[x,y] == 0: #if wall is found stop searching the lines
                    self.grid[x,y] = 2
                    self.gridnew.append([2,x,y])            ### [value, x, y]
                    break
                elif self.world[x,y] == 3: # Observer is found
                    self.grid[x,y] = 3
                    self.gridnew.append([3,x,y])
                    
                else:
                    self.grid[x,y] = 1
                    self.gridnew.append([1,x,y])

    def check_observers(self,x,y):
        new_observer = False
        found_num = 0
        if len(self.observers_known) > 0:       ##else check its a new observer
            
            for i in range(len(self.observer_pos)):
                o_x = self.observer_pos[i][0]
                o_y = self.observer_pos[i][1]
                if o_x == x and o_y == y:
                    for j in range(len(self.observers_known)):
                        if self.observers_known[j][0] == i:
                            return new_observer, found_num
                    new_observer = True
                    found_num = i
                    self.observers_known.append([i,x,y,self.observer_pos[i][2]]) 

                   
        else:                            ##if we dont know where any observers are 
            for i in range(len(self.observer_pos)):     
                o_x = self.observer_pos[i][0]
                o_y = self.observer_pos[i][1]
                if o_x == x and o_y == y:
                    self.observers_known.append([i,x,y,self.observer_pos[i][2]])
                    new_observer = True
                    

        return new_observer, found_num
    # def drawobservers(self):



    def drawmap(self, background,front):
        
        # self.frontier.map_update(self.grid)
        # front = self.frontier.get_frontiers()
        
        # print(len(self.gridnew))
        if len(self.gridbuffer) != 0:
            for i in range(len(self.gridbuffer)):
                x, y = self.gridbuffer[i][1], self.gridbuffer[i][2]

                color = GREY_TRANS

                if self.surfgrid[x,y].get_at((0,0)) != color:
                    self.surfgrid[x,y].fill(color)
                    self.map.blit(self.surfgrid[x,y],(self.size*x, self.size*y, self.size, self.size))
            
            self.gridbuffer.clear()


        # update current view
        for i in range(len(self.gridnew)):
            # if self.gridnew[i][0] == 0:
            #         # print("grey")
            #     color = (128, 128, 128, 127)

            x, y = self.gridnew[i][1], self.gridnew[i][2]

            self.gridbuffer.append(self.gridnew[i])

            if self.gridnew[i][0] == 1:
                color = WHITE
            elif self.gridnew[i][0] == 2:
                color = BLACK
            elif self.gridnew[i][0] == 3:
                color = YELLOW
                ##update vision drawing from here




            self.surfgrid[x,y].fill(color)
            
            
            # if self.check_observers(x,y):
            #     for j in range(len(self.observers_known)):
            #         ob = self.observers_known[j][0]
            #         for k in range(self.observers_vision.shape[0]):
            #             for l in range(self.observers_vision.shape[1]):
            #                 x1,y1 = self.observers_vision[0,1], self.observers_vision[0,2]
            #                 if self.observers_vision[1,x,y] == ob:
            #                     color = YELLOW_TRANS
            #                     self.surfgrid[x1,y1].fill(color)
            
            self.map.blit(self.surfgrid[x,y],(self.size*x, self.size*y, self.size, self.size))
                                

        ### actual grid visual

        # for i in range(self.grid.shape[0]):
        #     for j in range(self.grid.shape[1]):
        #         if self.grid[i,j] == 1:
        #             color = WHITE
        #         elif self.grid[i,j] == 0:
        #             color = BLACK
        #         # elif self.grid[i,j] == 2:
        #         #     color = BLACK 
        #         else:
        #             color = GREY

        #         self.surfgrid[i,j].fill(color)
        #         self.map.blit(self.surfgrid[i,j], (self.size*i, self.size*j, self.size, self.size))

        ## Draw frontiers
        for i in range(len(front)):
            color = BLUE
            x, y = front[i][0], front[i][1]

            self.surfgrid[x,y].fill(color)
            self.map.blit(self.surfgrid[x,y],(self.size*x, self.size*y, self.size, self.size))

        background.blit(self.map,(0,0))

    def update(self,background):
        
        self.vision_check()

        # print(self.grid[self.get_coord()[0]-1,self.get_coord()[1]+1])
        # front = []
                
        if not self.goal:

            self.frontier.map_update(self.grid)

            # front = self.frontier.get_frontiers()
            self.front = self.frontier.get_frontiers_active(self.gridnew)
            # self.currentgoal = front[self.goalnum]

            # print(len(front))
            # print(front)

            if self.front:
                # self.currentgoal = front[self.goalnum]
                
                self.currentgoal = self.front[0]

                if (abs(self.get_coord()[1] - self.currentgoal[0]) < 1) and (abs(self.get_coord()[0] - self.currentgoal[1] ) < 1):
                    
                    self.currentgoal = self.front[1]
                # self.currentgoal = [10,10]
            else:
                self.front = self.frontier.get_frontiers()
                if self.front:
                    self.currentgoal = self.front[0]
 
            self.pathfinder.updateMap(self.grid)
            # self.pathfinder.updateGoal(front[self.goalnum])
            path = self.pathfinder.create_path(self.get_coord(),self.currentgoal)
            # print(path)
            self.set_path(path)
            # print("currentgoalnum ")
            # print(self.goalnum)
            self.goalnum += 1
            if self.path:
                print("next goal")
                self.goal = True
        elif ((abs(self.get_coord()[1] - self.currentgoal[0]) < 1) and (abs(self.get_coord()[0] - self.currentgoal[1] )< 1)): ### change to collision rect
                # print("next goal")
                self.goal = False
                print("goal reached")
        
        # print(self.goal)

        self.check_collisions()

        self.drawmap(background,self.front)
        self.pathfinder.update(background)
        
        # print(str(self.currentgoal)+str(self.get_coord())+str(self.direction)+str(self.speed) + str((self.get_coord()[1] - self.currentgoal[0]))+str( ((self.get_coord()[0] - self.currentgoal[1] ))))

        self.pos += self.direction * self.speed
        self.rect.center = self.pos
