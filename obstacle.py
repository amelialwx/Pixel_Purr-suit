import pygame
from random import randint

import settings as S


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, frames):
        super().__init__()

        if type == 'mouse':
            self.frames = frames
            yPos = S.FLOOR
        elif type == 'fly':
            self.frames = frames
            yPos = S.FLOOR - S.HIGH_OBSTACLE_OFFSET
        else:
            self.frames = frames
            yPos = S.FLOOR - S.MID_OBSTACLE_OFFSET 

        self.animationIndex = 0
        self.image = self.frames[self.animationIndex]
        self.rect = self.image.get_rect(midbottom= (randint(S.OBSTACLE_X[0], S.OBSTACLE_X[1]), yPos))

    def animationState(self):
        self.animationIndex += S.OBSTACLE_INCREMENTS
        if self.animationIndex >= len(self.frames):
            self.animationIndex = 0
        self.image = self.frames[int(self.animationIndex)]

    def update(self):
        self.animationState()
        self.rect.x -= S.OBSTACLE_Y_INCREMENTS 
        self.destroy()
    
    def destroy(self):
        if self.rect.x < -100:
            self.kill()