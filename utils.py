
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