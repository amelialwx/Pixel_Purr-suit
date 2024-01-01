import pygame

import settings as S


class Player(pygame.sprite.Sprite):
    def __init__(self, runFrames, jumpFrames):
        super().__init__()
        self.playerRunFrames = runFrames
        self.playerJumpFrames = jumpFrames

        self.runAnimationIndex = 0
        self.jumpAnimationIndex = 0
        self.player_jump = self.playerJumpFrames[self.jumpAnimationIndex]
        self.image = self.playerRunFrames[self.runAnimationIndex]
        self.rect = self.image.get_rect(midbottom=(S.PLAYER_X, S.FLOOR))
        self.gravity = 0

        self.jumpSound = pygame.mixer.Sound(S.JUMP_AUDIO_PATH)
        self.jumpSound.set_volume(S.VOLUME)

    def playerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= S.FLOOR:
            self.gravity = S.GRAVITY
            self.jumpSound.play()

    def applyGravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= S.FLOOR:
            self.rect.bottom = S.FLOOR

    def animationState(self):
        if self.rect.bottom < S.FLOOR:
            self.jumpAnimationIndex += S.PLAYER_JUMP_INCREMENTS
            if self.jumpAnimationIndex >= len(self.playerJumpFrames):
                self.jumpAnimationIndex = 0
            self.image = self.playerJumpFrames[int(self.jumpAnimationIndex)]
        else:
            self.jumpAnimationIndex = 0
            self.runAnimationIndex += S.PLAYER_RUN_INCREMENTS
            if self.runAnimationIndex >= len(self.playerRunFrames):
                self.runAnimationIndex = 0
            self.image = self.playerRunFrames[int(self.runAnimationIndex)]

    def update(self):
        self.playerInput()
        self.applyGravity()
        self.animationState()