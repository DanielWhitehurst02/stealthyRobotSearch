
import pygame
import numpy as np

from settings import *

def draw_active_cell( map, screen):
    mouse_pos = pygame.mouse.get_pos()

    select_surf = pygame.Surface((screen.get_width(),screen.get_height()), pygame.SRCALPHA)

    row = int(mouse_pos[0]/ROBOT_WIDTH)
    col = int(mouse_pos[1]/ROBOT_WIDTH)
    # print(row, col)

    if (0 <= row) and (row < map.shape[0]) and (0 <= col) and (col < (map.shape[1])) :
        current_cell_value = map[row][col]
        
        if current_cell_value == 1:
            rect = pygame.Rect((row*ROBOT_WIDTH,col*ROBOT_WIDTH),(ROBOT_WIDTH,ROBOT_WIDTH))

            select_surf = pygame.image.load('select.png').convert_alpha()
            select_surf = pygame.transform.scale(select_surf,(ROBOT_WIDTH,ROBOT_WIDTH))
            # pygame.draw.rect(select_surf, YELLOW, rect )
            screen.blit(select_surf,rect)
            # print(row, col)

def drawtriangle(screen,mouse_pos,color):
        row = int(mouse_pos[0]/ROBOT_WIDTH)
        col = int(mouse_pos[1]/ROBOT_WIDTH)
        surf = pygame.Surface((screen.get_width(),screen.get_height()), pygame.SRCALPHA)
        rect = pygame.Rect((row*ROBOT_WIDTH,col*ROBOT_WIDTH),(ROBOT_WIDTH,ROBOT_WIDTH))

        # triangle = pygame.draw.polygon(surf,color,[((row*ROBOT_WIDTH) +(ROBOT_WIDTH/2),(col)*ROBOT_WIDTH),((row*ROBOT_WIDTH)-(ROBOT_WIDTH/2),(col*ROBOT_WIDTH)+(ROBOT_WIDTH/2)),((row*ROBOT_WIDTH)+(ROBOT_WIDTH),(col*ROBOT_WIDTH)+(ROBOT_WIDTH/2))])
        surf = pygame.image.load('select.png').convert_alpha()
        surf = pygame.transform.scale(surf,(ROBOT_WIDTH,ROBOT_WIDTH))
        
        screen.blit(surf,rect)

def getAngle(currentPos,newPos):
    angle = 0
    
    x = newPos[0]-currentPos[0]
    y = newPos[1]-currentPos[1]

    angle = np.rad2deg(np.arctan2(y,x))

    print(angle)
    return angle


def group_adjacents(frontiersqueue):
    search = True
    # i = 0
    grouped = []
    current_group = []
    adjacent = True
    while search:
        
        if frontiersqueue:
            

            if current_group:
                while adjacent:
                    adjacent = False
                    for j in range(len(current_group)):
                        # print(current_group)
                        for h in range(len(frontiersqueue)):
                            # print( str(h) + " len: " + str(len(frontiersqueue)))
                            if h >= (len(frontiersqueue)):
                                continue
                            x_o, y_o = current_group[j][0],current_group[j][1]
                            x_1, y_1 = frontiersqueue[h][0],frontiersqueue[h][1]
                            # if x_o == x_1 and y_o == y_1:
                            # print(str(abs(x_o - x_1))+str(abs(y_o - y_1)))
                            if (abs(x_o - x_1) <= 1 and abs(y_o - y_1) <= 1):
                                
                                adjacent = True
                                current_group.append(frontiersqueue[h])
                                del frontiersqueue[h]
                
                grouped.append(current_group)
                current_group = []
                
                        


            else:
                current_group.append(frontiersqueue[0])
                del frontiersqueue[0]
                adjacent = True
        else:
            search = False
    return grouped