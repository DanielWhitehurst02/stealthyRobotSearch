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


environment = 'office_space'

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
observer.draw_vision(screen,YELLOW_TRANS)
observer.update_vision(screen)

data1 = 'office_weightingstealth'
data2 = 'office_nostealth'
data3 = 'office_stealth_only'
data4 = 'office_weighting_disreguard'



with open(data1, 'rb') as weight_stealthy: 
    path_stealth, time_seen_stealth, number_time_seen_stealth, percent_explored_stealth, x_axis_stealth = pickle.load(weight_stealthy)
    # path_stealth, time_seen_stealth, number_time_seen_stealth, percent_explored_stealth, x_axis_stealth, map_stealth = pickle.load(weight_stealthy) 


with open(data2, 'rb') as no_stealth: 
    path_no_stealth, time_seen_no_stealth, number_time_seen_no_stealth, percent_explored_no_stealth, x_axis_no_stealth = pickle.load(no_stealth)
    # path_no_stealth, time_seen_no_stealth, number_time_seen_no_stealth, percent_explored_no_stealth, x_axis_no_stealth, map_no_stealth = pickle.load(no_stealth)

with open(data3, 'rb') as no_stealth: 
    path_stealth_only, time_seen_stealth_only, number_time_seen_stealth_only, percent_explored_stealth_only, x_axis_stealth_only = pickle.load(no_stealth)
    # path_stealth_only, time_seen_stealth_only, number_time_seen_stealth_only, percent_explored_stealth_only, x_axis_stealth_only, map_stealth_only = pickle.load(no_stealth)




with open(data4, 'rb') as no_stealth: 
    path_stealth_disreguard, time_seen_stealth_disreguard, number_time_seen_stealth_disreguard, percent_explored_stealth_disreguard, x_axis_stealth_disreguard, map_stealth_disreguard = pickle.load(no_stealth) 
    # print(path) 
    # print(time_seen)
#  navgrid.drawgrid(screen)

points = []
color = (255, 0, 0,255)
# step = 255/len(path_no_stealth)
step = 0
for i in range(len(path_no_stealth)):
    color =( (255 - step*i), 0, (0 + step*i), 255)
    # print(color)
    x, y = path_no_stealth[i][1], path_no_stealth[i][0]

    # xl = (x * ROBOT_WIDTH) + (ROBOT_WIDTH/2)
    # yl= (y * ROBOT_WIDTH) + (ROBOT_WIDTH/2)

    # points.append((xl,yl))
    pygame.draw.rect(screen,color,(ROBOT_WIDTH*x, ROBOT_WIDTH*y, ROBOT_WIDTH, ROBOT_WIDTH))

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


x = x_axis_stealth
time_seen = time_seen_stealth
number_time_seen = number_time_seen_stealth
percnt_xplore = percent_explored_stealth
total_time = x[len(x)-1]
print(total_time)

fig, ((ax1, ax2,ax3)) = plt.subplots(1, 3)

fig.suptitle(data1)
ax1.plot(x, time_seen)
ax1.set_title("Time Seen")
ax1.set(xlabel = "Time Seen (Steps)", ylabel = "Time (Steps)")


ax2.plot(x, number_time_seen, 'tab:orange')
ax2.set_title("Number of Times Seen")
ax2.set(xlabel = "Number of Times Seen", ylabel = "Time (Steps)")


ax3.plot(x, percnt_xplore, 'tab:green')
ax3.set_title("Percentage of environment explored")
ax3.set(xlabel = "Percentage explored (%)", ylabel = "Time (Steps)")

strategies = [data1,data2,data3]
total_time_list = [x_axis_stealth[len(x_axis_stealth)-1],x_axis_no_stealth[len(x_axis_no_stealth)-1],x_axis_stealth_only[len(x_axis_stealth_only)-1]]

plt.figure(2)
plt.bar(strategies,total_time_list,color= ['blue','orange','green'])
add_labels(strategies,total_time_list)

plt.figure(3)
plt.plot(x_axis_stealth, time_seen_stealth, x_axis_no_stealth, time_seen_no_stealth )
# ax4.plot(x_axis_stealth, -y**2, 'tab:red')


# observer.draw_vision(screen,YELLOW_TRANS)

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
        
