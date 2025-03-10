#!/usr/bin/env python3
import pygame
import math

from sys import exit
from settings import *

pygame.init()

#create window

screen = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Stealthy Robot")
clock = pygame.time.Clock()

#Background
white = (255,255,255)
red = (255,0,0)

class Robot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10,10])
        self.image.fill(red)
        self.pos = pygame.math.Vector2(ROBOT_START_X,ROBOT_START_Y)

robot = Robot()

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill(white)

    screen.blit(robot.image,robot.pos)

    pygame.display.update()
    clock.tick(FPS)
    