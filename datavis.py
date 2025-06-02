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



# environment = 'warehouse'
environment = 'openroom'
# environment = 'hallways'

with open(environment, 'rb') as inf: 
    ob_pos, env = pickle.load(inf)

print(ob_pos)

background = pygame.image.load(env)
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

pos_temp = []
finished = True



print(ob_pos)

# pathfinder = Pathfinder(navgrid.grid,goal,robwidth)
# robot = Robot(robwidth, navgrid.get_grid(), screen)

# print(navgrid.get_grid())

navgrid.drawgrid(screen)

observer = Observers(navgrid.get_grid(),360,ob_pos,PURPLE,screen)
# robot.visionmmap(screen)
for i in range(len(ob_pos)):
    x, y = ob_pos[i][1], ob_pos[i][0]
    pygame.draw.rect(screen,GREEN,(ROBOT_WIDTH*x, ROBOT_WIDTH*y, ROBOT_WIDTH*1.5, ROBOT_WIDTH*1.5))
    print(i)


vision = observer.vision()

observer.add_observers_tomap(navgrid.get_grid())
observer.def_vision_map()


# data1 = 'office_weightingstealth'
# data2 = 'office_nostealth'
# data3 = 'office_stealth_only'
# data4 = 'office_weighting_disreguard'


strategy1 = "weighting_disreguard"
strategy2 = "no_stealth"
strategy3 = "stealth_only"
strategy4 = "weighting"
# strategy5 = "weighting_disreguard_midpoint_front"
# strategy6 = "weighting_disreguard_near_front"


data1 = (environment+'_'+strategy1)
data2 = (environment+'_'+strategy2)
data3 = (environment+'_'+strategy3)
data4 = (environment+'_'+strategy4)
# data5 = (environment+'_'+strategy5)
# data6 = (environment+'_'+strategy6)
# # data3 = 'warehouse_no_stealth'

with open(data1, 'rb') as weight_stealthy: 
    path_stealth_disreguard, time_seen_stealth_disreguard, number_time_seen_stealth_disreguard, percent_explored_stealth_disreguard, x_axis_stealth_disreguard, map_stealth_disreguard = pickle.load(weight_stealthy) 

no_stealth = open(data2, 'rb')
    # path_no_stealth, time_seen_no_stealth, number_time_seen_no_stealth, percent_explored_no_stealth, x_axis_no_stealth = pickle.load(no_stealth)
path_no_stealth, time_seen_no_stealth, number_time_seen_no_stealth, percent_explored_no_stealth, x_axis_no_stealth, map_no_stealth = pickle.load(no_stealth)
no_stealth.close

stealth_only =  open(data3, 'rb') 
    # path_stealth, time_seen_stealth, number_time_seen_stealth, percent_explored_stealth, x_axis_stealth = pickle.load(weight_stealthy)
path_stealth, time_seen_stealth, number_time_seen_stealth, percent_explored_stealth, x_axis_stealth, map_stealth = pickle.load(stealth_only)
stealth_only.close()

with open(data4, 'rb') as weighting: 
    # path_stealth_only, time_seen_stealth_only, number_time_seen_stealth_only, percent_explored_stealth_only, x_axis_stealth_only = pickle.load(no_stealth)
    path_weight, time_seen_weight, number_time_seen_weight, percent_explored_weight, x_axis_stealth_weight, map_stealth_weight = pickle.load(weighting)
print(path_no_stealth)
 

print(path_stealth == path_no_stealth)
    # print(path) 
    # print(time_seen)
#  navgrid.drawgrid(screen)

points = []
color = (255, 0, 0,255)
step = 255/len(path_weight)
# step = 0
# for i in range(len(path_weight)):
#     color =( (255 - step*i), 0, (0 + step*i), 255)
#     # print(color)
#     x, y = path_weight[i][1], path_weight[i][0]

#     # xl = (x * ROBOT_WIDTH) + (ROBOT_WIDTH/2)
#     # yl= (y * ROBOT_WIDTH) + (ROBOT_WIDTH/2)

#     # points.append((xl,yl))
#     pygame.draw.rect(screen,color,(ROBOT_WIDTH*x, ROBOT_WIDTH*y, ROBOT_WIDTH, ROBOT_WIDTH))


# for i in range(len(path_weight)):
#     # color =( (255 - step*i), 0, (0 + step*i), 255)
#     # print(color)
#     x, y = path_weight[i][1], path_weight[i][0]

#     # xl = (x * ROBOT_WIDTH) + (ROBOT_WIDTH/2)
#     # yl= (y * ROBOT_WIDTH) + (ROBOT_WIDTH/2)

#     # points.append((xl,yl))
#     pygame.draw.rect(screen,BLUE,(ROBOT_WIDTH*x, ROBOT_WIDTH*y, ROBOT_WIDTH, ROBOT_WIDTH))


# for i in range(len(path_stealth_disreguard)):
#     # color =( (255 - step*i), 0, (0 + step*i), 255)
#     # print(color)
#     x, y = path_stealth_disreguard[i][1], path_stealth_disreguard[i][0]

#     # xl = (x * ROBOT_WIDTH) + (ROBOT_WIDTH/2)
#     # yl= (y * ROBOT_WIDTH) + (ROBOT_WIDTH/2)

#     # points.append((xl,yl))
#     pygame.draw.rect(screen,GREEN,(ROBOT_WIDTH*x, ROBOT_WIDTH*y, ROBOT_WIDTH, ROBOT_WIDTH))    
# pygame.draw.lines(screen,RED,False,points,5)




### plotting
# plt.figure(1)
# plt.subplot(211)

# plt.plot(x_axis_stealth,time_seen_stealth)
# plt.xlabel(' Time (steps)')
# plt.ylabel("time in vision")

# plt.subplot(212)
# plt.plot(x_axis_stealth,number_time_seen_stealth)
# plt.xlabel(' Time (steps)')
# plt.ylabel("times seen")

# plt.subplot(221)
# plt.plot(x_axis_stealth,percent_explored_stealth)
# plt.xlabel(' Time (steps)')
# plt.ylabel('Exploration Percentage (%)')

def add_labels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i] // 2, y[i], ha='center')  # Placing text at half the bar height

strategies = [strategy4,strategy1,strategy2,strategy3]

# x = x_axis_stealth
# time_seen = time_seen_stealth
# number_time_seen = number_time_seen_stealth
# percnt_xplore = percent_explored_stealth
# total_time = x[len(x)-1]
# print(percent_explored_no_stealth)
# print(x_axis_no_stealth)

# fig, ((ax1, ax2,ax3)) = plt.subplots(1, 3)
fig1 = plt.figure(1)

plt.suptitle(environment)

plt.subplot(2,2,1)
plt.plot(x_axis_stealth_weight,time_seen_weight)
plt.plot(x_axis_stealth_disreguard, time_seen_stealth_disreguard)
plt.plot(x_axis_no_stealth,time_seen_no_stealth)
plt.plot(x_axis_stealth,time_seen_stealth)


plt.title("Stealth cost over time")
plt.ylabel("Stealth cost") 
plt.xlabel("Time (Steps)")

plt.subplot(2,2,2)
plt.plot(x_axis_stealth_weight,number_time_seen_weight)
plt.plot(x_axis_stealth_disreguard, number_time_seen_stealth_disreguard, x_axis_no_stealth,number_time_seen_no_stealth, x_axis_stealth,number_time_seen_stealth)
plt.title("Number of Times Seen")
plt.ylabel("Number of Times Seen")
plt.xlabel("Time (Steps)")

plt.subplot(2,2,3)
plt.plot(x_axis_stealth_weight,percent_explored_weight)
plt.plot(x_axis_stealth_disreguard, percent_explored_stealth_disreguard, x_axis_no_stealth,percent_explored_no_stealth, x_axis_stealth,percent_explored_stealth)
plt.title("Percentage of environment explored")
plt.ylabel("Percentage explored (%)")
plt.xlabel ("Time (Steps)")



# print(x_axis_no_stealth[len(x_axis_no_stealth)-1])


total_time_list = [x_axis_stealth_weight[len(x_axis_stealth_weight)-1],x_axis_stealth_disreguard[len(x_axis_stealth_disreguard)-1],x_axis_no_stealth[len(x_axis_no_stealth)-1],x_axis_stealth[len(x_axis_stealth)-1]]
plt.subplot(2,2,4)
# plt.figure(2)
plt.bar(strategies,total_time_list,color= ['blue','orange','green', 'red'])
plt.title("Time to explore environment")
add_labels(strategies,total_time_list)

fig1.legend(strategies)

# fig2 = plt.figure(2)
# plt.plot(x_axis_stealth_disreguard,time_seen_stealth_disreguard ,x_axis_stealth_weight,time_seen_weight)


# with open(data6, 'rb') as mid: 
#     # path_stealth_only, time_seen_stealth_only, number_time_seen_stealth_only, percent_explored_stealth_only, x_axis_stealth_only = pickle.load(no_stealth)
#     path_mid, time_mid, number_mid, percent_mid, x_axis_mid, map_mid = pickle.load(mid)
# print(path_no_stealth)

# with open(data6, 'rb') as near: 
#     # path_stealth_only, time_seen_stealth_only, number_time_seen_stealth_only, percent_explored_stealth_only, x_axis_stealth_only = pickle.load(no_stealth)
#     path_near, time_near, number_near, percent_near, x_axis_near, map_near = pickle.load(near)
# print(path_no_stealth)


# plt.figure(2)
# plt.plot(x_axis_mid,time_mid,x_axis_stealth_disreguard,time_seen_stealth_disreguard)
# # plt.plot(x_axis_stealth_disreguard, time_seen_stealth_disreguard)
# plt.plot(x_axis_stealth,time_seen_stealth,label='Curve 1')
# # plt.plot(x_axis_no_stealth,time_seen_no_stealth,label='Curve 2')


# plt.title("Time Seen")
# plt.ylabel("Time Seen (Steps)") 
# plt.xlabel("Time (Steps)")


# plt.figure(4)

# # plt.plot(x_axis_stealth_disreguard, time_seen_stealth_disreguard)
# # plt.plot(x_axis_stealth,time_seen_stealth,label='Curve 1')
# plt.plot(x_axis_no_stealth,time_seen_no_stealth,label='Curve 2')


# plt.title("Time Seen")
# plt.ylabel("Time Seen (Steps)") 
# plt.xlabel("Time (Steps)")

# plt.figure(3)
# plt.plot(x_axis_stealth, time_seen_stealth, x_axis_no_stealth, time_seen_no_stealth )
# # ax4.plot(x_axis_stealth, -y**2, 'tab:red')

## average stuff

# average_weight = 0
# average_disreguard = 0

# average_stealth = 0
# average_no_stealth = 0

# for i in range(3):
#     if i == 0:
#         environment = 'warehouse'
#     elif i == 1:
#         environment = 'hallways'
#     else:   
#         environment = 'openroom'

#     data1 = (environment+'_'+strategy1)
#     data2 = (environment+'_'+strategy2) 
#     data3 = (environment+'_'+strategy3)
#     data4 = (environment+'_'+strategy4)

#     with open(data1, 'rb') as weight_stealthy: 
#         path_stealth_disreguard, time_seen_stealth_disreguard, number_time_seen_stealth_disreguard, percent_explored_stealth_disreguard, x_axis_stealth_disreguard, map_stealth_disreguard = pickle.load(weight_stealthy) 

#     no_stealth = open(data2, 'rb')
#         # path_no_stealth, time_seen_no_stealth, number_time_seen_no_stealth, percent_explored_no_stealth, x_axis_no_stealth = pickle.load(no_stealth)
#     path_no_stealth, time_seen_no_stealth, number_time_seen_no_stealth, percent_explored_no_stealth, x_axis_no_stealth, map_no_stealth = pickle.load(no_stealth)
#     no_stealth.close

#     stealth_only =  open(data3, 'rb') 
#         # path_stealth, time_seen_stealth, number_time_seen_stealth, percent_explored_stealth, x_axis_stealth = pickle.load(weight_stealthy)
#     path_stealth, time_seen_stealth, number_time_seen_stealth, percent_explored_stealth, x_axis_stealth, map_stealth = pickle.load(stealth_only)
#     stealth_only.close()

#     with open(data4, 'rb') as weighting: 
#         # path_stealth_only, time_seen_stealth_only, number_time_seen_stealth_only, percent_explored_stealth_only, x_axis_stealth_only = pickle.load(no_stealth)
#         path_weight, time_seen_weight, number_time_seen_weight, percent_explored_weight, x_axis_stealth_weight, map_stealth_weight = pickle.load(weighting)
#     # print(path_no_stealth)

#     # average_weight += time_seen_weight[len(time_seen_weight)-1]
#     # average_disreguard += time_seen_stealth_disreguard[len(time_seen_stealth_disreguard)-1]
#     # average_stealth += time_seen_stealth[len(time_seen_stealth)-1]
#     # average_no_stealth += time_seen_no_stealth[len(time_seen_no_stealth)-1]

#     average_weight += x_axis_stealth_weight[len(x_axis_stealth_weight)-1]
#     average_disreguard += x_axis_stealth_disreguard[len(x_axis_stealth_disreguard)-1]
#     average_stealth += x_axis_stealth[len(x_axis_stealth)-1]
#     average_no_stealth += x_axis_no_stealth[len(x_axis_no_stealth)-1]

# average_weight = average_weight/3
# average_disreguard = average_disreguard/3
# average_stealth = average_stealth/3
# average_no_stealth = average_no_stealth/3

# averages = [round(average_weight),round(average_disreguard),round(average_no_stealth),round(average_stealth)]
# # averages = [average_weight,average_disreguard,average_stealth,average_no_stealth]
# print(averages)

# fig2 = plt.figure(2)
# # plt.plot(x_axis_stealth_disreguard,time_seen_stealth_disreguard ,x_axis_stealth_weight,time_seen_weight)
# plt.bar(strategies,averages,color= ['blue','orange','green', 'red'])
# plt.title("average total exploration time")
# add_labels(strategies,averages)
# plt.ylabel("total exploration time (steps)")
# plt.show()

# observer.draw_vision(screen,YELLOW_TRANS)


        ### actual grid visual
# map = map_stealth_weight
map = map_stealth
# map = map_stealth_disreguard

for i in range(map.shape[0]):
    for j in range(map.shape[1]):
        if map[i,j] == 1:
            color = WHITE
        elif map[i,j] == 2:
            color = BLACK
        # elif self.grid[i,j] == 2:
        #     color = BLACK 
        elif map[i,j] == 0:
            color = GREY
        elif map[i,j] == 3:
            color = GREEN

        pygame.draw.rect(screen,color,(ROBOT_WIDTH*i, ROBOT_WIDTH*j, ROBOT_WIDTH, ROBOT_WIDTH))


# for i in range(len(path_stealth_disreguard)):
#     # color =( (255 - step*i), 0, (0 + step*i), 255)
#     # print(color)
#     x, y = path_stealth_disreguard[i][1], path_stealth_disreguard[i][0]

#     # xl = (x * ROBOT_WIDTH) + (ROBOT_WIDTH/2)
#     # yl= (y * ROBOT_WIDTH) + (ROBOT_WIDTH/2)

#     # points.append((xl,yl))
#     pygame.draw.rect(screen,RED,(ROBOT_WIDTH*x, ROBOT_WIDTH*y, ROBOT_WIDTH, ROBOT_WIDTH))


for i in range(len(path_weight)):
    # color =( (255 - step*i), 0, (0 + step*i), 255)
    # print(color)
    x, y = path_weight[i][1], path_weight[i][0]

    # xl = (x * ROBOT_WIDTH) + (ROBOT_WIDTH/2)
    # yl= (y * ROBOT_WIDTH) + (ROBOT_WIDTH/2)

    # points.append((xl,yl))
    pygame.draw.rect(screen,BLUE,(ROBOT_WIDTH*x, ROBOT_WIDTH*y, ROBOT_WIDTH, ROBOT_WIDTH))

# for i in range(len(path_stealth)):
#     # color =( (255 - step*i), 0, (0 + step*i), 255)
#     # print(color)
#     x, y = path_stealth[i][1], path_stealth[i][0]

#     # xl = (x * ROBOT_WIDTH) + (ROBOT_WIDTH/2)
#     # yl= (y * ROBOT_WIDTH) + (ROBOT_WIDTH/2)

#     # points.append((xl,yl))
#     pygame.draw.rect(screen,GREEN,(ROBOT_WIDTH*x, ROBOT_WIDTH*y, ROBOT_WIDTH, ROBOT_WIDTH))


# observer.draw_vision(screen,YELLOW_TRANS)
# observer.update_vision(screen)


pygame.display.update()

while True:

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            plt.show()
            pygame.quit()
            exit()
   


    pygame.display.flip()
    clock.tick(FPS)
        
