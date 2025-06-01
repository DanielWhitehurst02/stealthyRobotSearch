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
        self.rect = self.image.get_rect(center=(ROBOT_START_X*size,ROBOT_START_Y*size))
        
        #movement
        # self.pos = pygame.math.Vector2(ROBOT_START_X,ROBOT_START_Y)
        self.pos = [ROBOT_START_X,ROBOT_START_Y]
        self.speed = SPEED
        # self.direction = pygame.math.Vector2(0,0)
        self.direction = [0,0]

        #path
        self.path = []
        self.collision_rects = []
        self.grid = []
        self.viewdist = ROBOT_VISION_LENGTH
        self.fov = ROBOT_FOV

        self.world = world

        self.map = pygame.Surface((background.get_width(),background.get_height()),pygame.SRCALPHA)

        self.frontier = Frontier(self.grid)
        self.pathfinder = Pathfinder(self.grid,size)

        self.goal = False
        self.goalnum = 0
        self.steps = 0


        
        #Observers

        self.observer_pos = observer_pos
        print(self.observer_pos)
        self.observers_known = []

        for i in range(len(observer_pos)):
            self.observers_known.append(False)

        self.observers_vision = observers_vision_map
        self.observers_vision_known = []
        for i in range(len(observers_vision_map)):
            self.observers_vision_known.append(0)

        ## Evaluation ##
        self.percent_explored = 0
        self.number_times_seen = 0
        self.time_seen = 0
        self.prev_seen = False
        self.eval_path = []
        self.time = 0

        self.observer_seen = False

        self.wallthreshold = WALL_THRESHOLD

        self.get_map_combined_ground_truth()


    def get_coord(self):
        col = self.rect.centery // self.size
        row = self.rect.centerx // self.size
        return col,row
    
    def set_path(self, path):
        self.path = path
        self.create_collision_rects()
        # self.get_direction()
        self.get_direction_snapped()
        
    def set_observervision(self, observers_vision_map):
        self.observers_vision = observers_vision_map
    
    def create_collision_rects(self):
        if self.path:
            self.collision_rects = []
            # print(self.path)
            # for point in self.path: 
            #     # x = (point.x *self.size) + (self.size/2)
            #     # y = (point.y *self.size) + (self.size/2)
            #     x = (point.x * self.size)
            #     y = (point.y * self.size)

            #     # rect = pygame.Rect((y-(self.size/4),x-(self.size/4)),((self.size/2),(self.size/2)))
            #     rect = pygame.Rect((y-(self.size),x-(self.size)),((self.size),(self.size)))
            #     self.collision_rects.append(rect)

            for point in self.path: 
                y = (point.x)
                x = (point.y)

                # print("point in path: " + str(x) +" , "+ str(y))

                # # rect = pygame.Rect((y-(self.size/4),x-(self.size/4)),((self.size/2),(self.size/2)))
                # rect = pygame.Rect((y-(self.size),x-(self.size)),((self.size),(self.size)))
                self.collision_rects.append([x,y])

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


        print("self dircetion: " +str(self.direction))

    def get_direction_snapped(self):
        # start_x,start_y = self.pos[0], self.pos[1]
        if self.collision_rects:
            end = self.collision_rects[0]
            
            # self.direction[0] = end[0] - int(start_x/self.size)
            # self.direction[1] = end[1] - int(start_y/self.size)

            self.direction[0] = end[0] - self.pos[0]
            self.direction[1] = end[1] - self.pos[1]

            # print ( "end: " +str(end) + " pos: " + str(self.pos) + " Direction: " + str(self.direction))
            # self.direction = end - self.pos
        else:
            self.direction= [0,0]

    def closest_frontier(self, pos): 
        dist = math.dist([pos[1],pos[0]],[self.front[0][0],self.front[0][1]])
        short_i = 0
        for i in range(len(self.front)):
            temp_dist = math.dist([pos[1],pos[0]],[self.front[i][0],self.front[i][1]])
            
            if temp_dist < dist:
                dist = temp_dist
                short_i = i
        
        return short_i, dist
                    # print(str(temp_dist) +" Index: "+str(i))

    def closest_frontier_shortest_path(self, pos): ## TODO calculate closest frontier by path dist
        dist = math.dist([pos[1],pos[0]],[self.front[0][0],self.front[0][1]])
        # dist = 100
        short_i = 0
        short_i_queue = [0,0,0,0,0]
        short_path = []

        stealth_cost = 100000000
        info_gain = 0

        # front_value = 0

        queue = []

        for i in range(len(self.front)):
            # temp_dist = math.dist([pos[1],pos[0]],[self.front[i][0],self.front[i][1]])
            # heuristic = [self.front[i][0],self.front[i][1]]
            temp_path = self.pathfinder.create_path(pos, self.front[i])
            temp_dist = len(temp_path)
            temp_stealth_cost = 0
            
            temp_info_gain = self.frontier_info_gain([self.front[i][1],self.front[i][0]])
            # print(info_gain)
            for point in temp_path: 
                y = (point.x)
                x = (point.y)
                if ROBOT_PATHFINDING_AVOID_VISION:
                    temp_stealth_cost += self.map_combined[x,y]

            queue.append([temp_info_gain,temp_stealth_cost,temp_dist])

            # print(str(temp_dist) + " queueval: " + str(queue[i][2]))

            # # print(temp_dist)

            # if temp_dist < dist:
            #     dist = temp_dist
            #     # short_path = temp_path
            #     short_i_queue[4] = short_i_queue[3]
            #     short_i_queue[3] = short_i_queue[2]
            #     short_i_queue[2] = short_i_queue[1]
            #     short_i_queue[1] = short_i
            #     short_i_queue[0] = i
            #     short_i = i

            # if temp_stealth_cost < stealth_cost:
            #     dist = temp_dist
            #     stealth_cost = temp_stealth_cost
            #     short_path = temp_path
            #     short_i = i

        for i in range(len(queue)):
            
                # continue
            
            # info_temp = np.power(math.e,(-0.01*(INFO_GAIN*queue[i][0])))
            # info_temp = 2 * math.log(INFO_GAIN*queue[i][0])
            info_temp = INFO_GAIN*queue[i][0]
            # info_temp = math.sqrt(INFO_GAIN*queue[i][0])
            stealth_temp = (STEALTH_COST*queue[i][1])
            dist_temp = (DIST_WEIGHT*queue[i][2])

            # front_value_temp =  info_temp + stealth_temp + dist_temp
            # front_value_temp = info_temp - stealth_temp
            # front_value_temp = (info_temp)/(pow(dist_temp,2)) - stealth_temp
            
            # front_value_temp = (info_temp-stealth_temp)/(pow(dist_temp,1.3))

            front_value_temp = (info_temp)/(pow(dist_temp,1.3))-stealth_temp

            if i == 0:
                front_value = front_value_temp

            print("Info_gain: " + str(info_temp) + " Stealth cost: " + str(stealth_temp) + " DIST value: " + str(dist_temp) + " Front value: " + str(front_value_temp) + " Index: " + str(i))

            if front_value_temp > front_value:
                dist = queue[i][2]
                # stealth_cost = temp_stealth_cost
                front_value = front_value_temp
                short_path = temp_path
                short_i = i
        # for j in range(len(short_i_queue)):
        #     i = short_i_queue[j]

        #     temp_path = self.pathfinder.create_path(pos, self.front[i])
        #     temp_dist = len(temp_path)
        #     temp_stealth_cost = 0
            
        #     for point in temp_path: 
        #         y = (point.x)
        #         x = (point.y)
        #         temp_stealth_cost += self.map_combined[x,y]


        #     if temp_stealth_cost < stealth_cost:
        #         dist = temp_dist
        #         stealth_cost = temp_stealth_cost
        #         short_path = temp_path
        #         short_i = i

        print( "selecting index: " + str(short_i))
        return short_i, dist, short_path
                    # print(str(temp_dist) +" Index: "+str(i))

    def frontier_info_gain(self, pos):
        info_gain= 0
        for theta in np.arange(0,self.fov,5):
            end_x, end_y = self.viewdist*math.cos(math.radians(theta)),self.viewdist*math.sin(math.radians(theta))
            endp = [(round((end_x) + pos[0])), (round((end_y) + pos[1]))]
            line = supercover_line(pos,endp)
            for i in range(len(line)):
                x, y = line[i][1],line[i][0]
                if x >= self.grid.shape[0] or y >= self.grid.shape[1] or x<0 or y<0: # disreguard out of range readings
                    break
                if self.grid[x,y] == 0:
                    info_gain += 1
                elif self.grid[x,y] == 2: #if wall is found stop searching the lines
                    break



        return info_gain


    def check_path(self):
        obstructed = False
        if self.path:
            for i in range(len(self.collision_rects)-1):
                val = self.grid[self.collision_rects[i][0]][self.collision_rects[i][1]]
                
                if val == 2:
                    obstructed = True
        return obstructed

    def check_collisions(self):
        if self.collision_rects:
                # start_x,start_y = int(self.pos[0]/self.size), int(self.pos[1]/self.size)
            # for rect in self.collision_rects:
                # if rect.collidepoint(self.pos):
                # #   print("real")
                #   del self.collision_rects[0]
                #   self.get_direction()
                # if [start_x,start_y] == self.collision_rects[0]:
                # print(self.pos == self.collision_rects[0])
                # print(self.pos)
                # print(self.collision_rects[0])
                if self.pos == self.collision_rects[0]:
                    del self.collision_rects[0]
                    # self.get_direction_snapped()

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
   
    def vision_check(self):
        self.gridnew.clear()

        x,y = self.pos[0],self.pos[1]

        if self.world[x,y] == 1:
            self.grid[x,y] = 1
            self.gridnew.append([2,x,y])
        
        for k in range(-1,2,1):            
            if x<0 or y<0: # disreguard out of range readings
                continue
            for l in range(-1, 2,1): ## check surrounding tiles
                if self.world[x+k,y+l] == 0: #if wall is found stop searching the lines
                    self.grid[x+k,y+l] = 2
                    self.gridnew.append([2,x+k,y+l])  ### [value, x, y]
                else:
                    self.grid[x+k,y+l] = 1
                    self.gridnew.append([1,x+k,y+l])            


        for theta in np.arange(0,self.fov,1):
            end_x, end_y = self.viewdist*math.cos(math.radians(theta)),self.viewdist*math.sin(math.radians(theta))
            endp = [(round((end_x) + self.get_coord()[0])), (round((end_y) + self.get_coord()[1]))]
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
                    self.check_observers(x,y)

                else:
                    self.grid[x,y] = 1
                    self.gridnew.append([1,x,y])  
                
        # return observer_seen

    def check_observers(self,x,y):

        for i in range(len(self.observer_pos)):
                o_x = self.observer_pos[i][1]
                o_y = self.observer_pos[i][0]

                # print(x,y,o_x,o_y)
                if o_x == x and o_y == y:

                    if not self.observers_known[i]:
                        if ROBOT_PATHFINDING_AVOID_VISION:
                            # print("new observer found")
                            self.observer_seen = True

                    self.observers_known[i] = True



        self.update_vision_map(self.observers_known)

        # return new_observer, found_num
        # for i in range(len(self.visionmap)):
    # def drawobservers(self):

    def update_vision_map(self,observers_know):
        for i in range(len(self.observers_vision)):
            if observers_know[i] == True:
                self.observers_vision_known[i] = self.observers_vision[i]
                
        # print(self.observers_vision_known)

    def get_map_combined(self):
        self.map_combined = np.zeros(shape=(self.grid.shape[0], self.grid.shape[1]))

        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.grid[i,j] == 1:
                    self.map_combined[i,j] = 1
                elif self.grid[i,j] == 0:
                    self.map_combined[i,j] = 50 ##-1 for unknown cell
                else:
                    self.map_combined[i,j] = 0
        
        if ROBOT_PATHFINDING_AVOID_VISION:
            #### TODO currently robot knows vision arcs of robot
            for i in range(len(self.observers_vision_known)):
                if self.observers_vision_known[i] != 0:
                    for j in range(len(self.observers_vision_known[i])):
                        x,y = self.observers_vision_known[i][j][0], self.observers_vision_known[i][j][1]
                        if self.observers_vision_known[i][j][2] > 0:
                            self.map_combined[x,y] += self.observers_vision_known[i][j][2]  

    def get_map_combined_ground_truth(self):
        self.map_combined_truth = np.zeros(shape=(self.world.shape[0], self.world.shape[1]))

        for i in range(self.world.shape[0]):
            for j in range(self.world.shape[1]):
                if self.world[i,j] == 1:
                    self.map_combined_truth[i,j] = 0 ## empty space
                else:
                    self.map_combined_truth[i,j] = 1 ## wall
        

        for i in range(len(self.observers_vision)):
            for j in range(len(self.observers_vision[i])):
                x,y = self.observers_vision[i][j][0], self.observers_vision[i][j][1]
                if self.observers_vision[i][j][2] > 0:
                    self.map_combined_truth[x,y] += self.observers_vision[i][j][2]  

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
                color = PURPLE
                ##update vision drawing from here
                # self.check_observers(x,y)



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

    ### Evaluation ####

    def get_percent_explored(self):
        unexploredtiles = 0
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.grid[i,j] == 0:
                    unexploredtiles +=1
        
        self.percent_explored =  1 - (unexploredtiles)/(self.grid.shape[0]*self.grid.shape[1])

        return self.percent_explored 
    
    def get_number_times_seen(self,x,y):
        # print(self.prev_seen)
        if self.map_combined_truth[y,x] > 1 and self.prev_seen == False:
            
            self.number_times_seen += 1

            self.prev_seen = True
        elif self.map_combined_truth[y,x] <= 1:
            self.prev_seen = False
    
    def get_time_seen(self,x,y):
        # print(self.map_combined[y,x])
        if self.map_combined_truth[y,x] > 1:
            self.time_seen += 1

    def save_path(self,x,y):
        self.eval_path.append([x,y])
    
    def get_eval(self):
        return self.eval_path, self.time_seen, self.number_times_seen, self.percent_explored
    
    ### Update Loop ###
    ## TODO update frontiers when observer is seen
    ##TODO Check path


    def update(self,background): 
        finished = False
        self.observer_seen = False
        self.vision_check()
        self.get_map_combined()

        # print(self.grid[self.get_coord()[0]-1,self.get_coord()[1]+1])
        # front = []

        pos = self.get_coord()
        
        # self.observer_seen = True
        # print("Value at pos: " + str(self.map_combined[pos[1]][pos[0]]))
        
        # print(self.observer_seen)
        path_clear = self.check_path()

        # if self.observer_seen:
        #     print("updating cause of observer detection")
        #     self.goal = False

        if path_clear:
            print("path blocked")
            # if len(self.collision_rects) <= 0:
            self.goal = False
            # elif self.grid[self.collision_rects[1][0]][self.collision_rects[1][1]] == 2:
            #     self.goal = False
                
        if not self.goal or self.steps >= UPDATE_STEPS or self.observer_seen :
            self.wallthreshold = WALL_THRESHOLD

            self.frontier.map_update(self.grid,self.gridnew)
            self.pathfinder.updateMap(self.map_combined)

            has_front = False

            while not has_front:

                self.front = self.frontier.get_frontiers(self.wallthreshold)

                if self.front:
                    findfrontier = True
                    while findfrontier:
                        short_i, dist, short_path = self.closest_frontier_shortest_path(pos)
                        # print(dist)
                        if dist < 0:
                            del self.front[short_i]
                            # short_i, dist = self.closest_frontier(pos)
                            findfrontier = True
                        else:
                            findfrontier = False


                    

                    self.currentfront = short_i
                    self.currentgoal = self.front[short_i]
                    has_front = True
                    
                else:
                    print(self.get_percent_explored())
                    print(self.get_percent_explored() > EXPLORE_PERCENT_FIN)

                    if self.get_percent_explored() > EXPLORE_PERCENT_FIN:
                        has_front = True
                        finished = True
                    else:
                        self.wallthreshold += 1
                # randx, randy = np.random.randint(-1,2),np.random.randint(-1,2)
                # print(randx)
                # self.currentgoal = [pos[1]+randx,pos[0]+randy]
                # self.currentgoal = [pos[1],pos[0]]
                # finished = True
                # has_front = True
            # print(self.currentgoal)

            # if short_path:
            #     path = short_path
            
            # self.pathfinder.updateMap(self.grid, [])
            # self.pathfinder.updateGoal(front[self.goalnum])
            # else:
            path = self.pathfinder.create_path(pos,self.currentgoal)
            # print(path)

            # if not path:
            #     # print("no path")
            #     # del self.front[short_i]
            #     # short_i, dist = self.closest_frontier(pos)
            #     # self.currentgoal = self.front[short_i]
            #     self.pathfinder.create_path(pos, self.currentgoal)

            self.set_path(path)
            # print("currentgoalnum ")
            # print(self.goalnum)

            #evaluation metrics

            print("Percentage Explored " + str(self.get_percent_explored()) +" Time seen: " + str(self.time_seen) + " Number of times seen: " + str(self.number_times_seen) )
            # print(self.observers_known)

            self.goalnum += 1
            if self.path:
                # print("next goal")
                self.goal = True

            self.steps = 0
        elif ((abs(pos[1] - self.currentgoal[0]) < 1) and (abs(pos[0] - self.currentgoal[1] )< 1)): ### change to collision rect
                # print("next goal")
                self.goal = False
                # del self.front[self.currentfront]
                # print("goal reached")
        
        
        self.get_direction_snapped()
        self.check_collisions()

        self.drawmap(background,self.front)
        self.pathfinder.update(background)
        
        #evaluation metrics

        # print(str(self.currentgoal)+str(self.get_coord())+str(self.direction)+str(self.speed) + str((self.get_coord()[1] - self.currentgoal[0]))+str( ((self.get_coord()[0] - self.currentgoal[1] ))))
        # print(self.pos)
        x, y = pos[0],pos[1]

        self.get_time_seen(x,y)
        self.get_number_times_seen(x,y)
        self.save_path(x,y)
        # print(self.time_seen)
        # print(self.number_times_seen)
        self.time += 1
        self.steps += 1

        # self.pos += (self.direction * self.speed)
        # print(str(self.pos)+" direct: " + str(self.direction))
        self.pos[0] += self.direction[0]
        self.pos[1] += self.direction[1]
        self.rect.center = [self.pos[0]*self.size,self.pos[1]*self.size]
        # self.rect.center = [int(self.pos[0]/self.size)*self.size,int(self.pos[1]/self.size)*self.size]
        # print(self.rect.center)
        return finished
