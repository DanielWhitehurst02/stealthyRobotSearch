
import pygame

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
            print(row, col)
        