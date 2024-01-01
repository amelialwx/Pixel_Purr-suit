import pygame
from sys import exit
import json
from random import randint, choice

import settings as S
from player import Player 
from obstacle import Obstacle
from spritesheet import SpriteSheet
    

def drawBackground():
    global bgX1, bgX2
    screen.blit(backgroundImage, (bgX1, 0))
    screen.blit(backgroundImage, (bgX2, 0))

    bgX1 -= S.BACKGROUND_X
    bgX2 -= S.BACKGROUND_X

    if bgX1 <= -newWidth:
        bgX1 = newWidth
    if bgX2 <= -newWidth:
        bgX2 = newWidth


def displayScore():
    currentTime = int(pygame.time.get_ticks() / 1000) - startTime
    scoreSurf = gameFontReg.render(f'Score: {currentTime}', False, S.SCORE_COLOR)
    scoreRect = scoreSurf.get_rect(center=(S.CURRENT_SCORE_X, S.CURRENT_SCORE_Y))
    screen.blit(scoreSurf, scoreRect)
    return currentTime


def displayFinalScore(text, font, position, color='white'):
    message = font.render(text, False, color)
    messageRect = message.get_rect(center=position)
    screen.blit(message, messageRect)


def spriteCollision():
    if pygame.sprite.spritecollide(player.sprite, obstacleGroup, False):
        obstacleGroup.empty()
        return False
    return True


def drawPauseScreen():
    translucentOverlay = pygame.Surface((S.SCREEN_WIDTH, S.SCREEN_HEIGHT)).convert_alpha()
    translucentOverlay.fill('grey')

    screen.blit(translucentOverlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    pausedText = gameFontReg.render('Paused', False, S.PAUSED_COLOR)
    pauseRect = pausedText.get_rect(center=(S.SCREEN_WIDTH/2, S.PAUSED_Y))
    screen.blit(pausedText, pauseRect)

    escapeText = gameFontReg.render('Press Escape to resume', False, S.ESCAPE_COLOR)
    escapeRect = escapeText.get_rect(center=(S.SCREEN_WIDTH/2, S.ESCAPED_Y))
    screen.blit(escapeText, escapeRect)


def loadSpriteFrames(imagePath, frameDetails):
    spritesheet = SpriteSheet(pygame.image.load(imagePath).convert_alpha())
    frames = [spritesheet.get_image(*details) for details in frameDetails]
    return frames


def drawIdleScreen(frames, idleFrameTimer):
    idleFrameTimer += S.IDLE_INCREMENTS
    if idleFrameTimer >= len(frames):
        idleFrameTimer = 0
    currentFrame = frames[int(idleFrameTimer)]
    if score !=0 or highscoreData['highscore'] != 0:
        screen.blit(currentFrame, currentFrame.get_rect(midbottom=(S.SCREEN_WIDTH/2, S.IDLE_SCORE_Y)))
    else:
        screen.blit(currentFrame, currentFrame.get_rect(midbottom=(S.SCREEN_WIDTH/2, S.IDLE_NO_SCORE_Y)))
    return idleFrameTimer


def updateHighscore():
    global score, highscoreData
    if score > highscoreData['highscore']:
        highscoreData['highscore'] = score


# Initialize the game
pygame.init()

pygame_icon = pygame.image.load('graphics/icon.png')
pygame.display.set_icon(pygame_icon)

# Game configuration
screen = pygame.display.set_mode((S.SCREEN_WIDTH, S.SCREEN_HEIGHT))
pygame.display.set_caption("Pixel Runner")

# FPS
clock = pygame.time.Clock()

# Game state flags
gameActive = False
gamePaused = False
overlayDrawn = False

# Score tracker
startTime = 0
pauseTime = 0
score = 0
# Highscore data
highscoreData = {'highscore': 0}
try:
    with open('highscore.json') as highscoreFile:
        highscoreData = json.load(highscoreFile)
except:
    None

# Game music
music = pygame.mixer.Sound(S.MUSIC_AUDIO_PATH)
music.play(loops = -1)

# Game font
gameFontBig = pygame.font.Font(S.FONT_PATH, S.GAME_FONT_BIG_SIZE)
gameFontReg = pygame.font.Font(S.FONT_PATH, S.GAME_FONT_REG_SIZE)
gameFontSm = pygame.font.Font(S.FONT_PATH, S.GAME_FONT_SM_SIZE)
gameFontXSm = pygame.font.Font(S.FONT_PATH, S.GAME_FONT_X_SM_SIZE)

# Initialize player sprite
player = pygame.sprite.GroupSingle()
playerRunFrames = loadSpriteFrames(S.RUN_SPRITESHEET_PATH, S.RUN_SPRITESHEET_ARGS)
playerJumpFrames = loadSpriteFrames(S.JUMP_SPRITESHEET_PATH, S.JUMP_SPRITESHEET_ARGS)
player.add(Player(playerRunFrames, playerJumpFrames))
playerIdleFrames = loadSpriteFrames(S.IDLE_SPRITESHEET_PATH, S.IDLE_SPRITESHEET_ARGS)

# Initialize obstacle sprites
obstacleGroup = pygame.sprite.Group()
fly1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
flyFrames = [fly1, fly2]
mouseFrames = loadSpriteFrames(S.MOUSE_SPRITESHEET_PATH, S.MOUSE_SPRITESHEET_ARGS)

# Load game background
backgroundSurf = pygame.image.load(S.BACKGROUND_PATH).convert()
backgroundAr = backgroundSurf.get_width() / backgroundSurf.get_height()
newWidth = int(backgroundAr * S.SCREEN_HEIGHT)
backgroundImage = pygame.transform.scale(backgroundSurf, (newWidth, S.SCREEN_HEIGHT))
bgX1 = 0
bgX2 = newWidth

# Intro screen
gameName = gameFontBig.render("Pixel Runner", False, S.GAME_NAME_COLOR)
gameNameRect = gameName.get_rect(center=(S.SCREEN_WIDTH/2, S.GAME_NAME_Y))

gameSubName = gameFontXSm.render(S.GAME_SUB_TEXT, False, S.GAME_NAME_COLOR)
gameSubRect = gameSubName.get_rect(center=(S.SCREEN_WIDTH/2, S.GAME_NAME_Y + 40))

startMsg = gameFontReg.render('Press space to run', False, 'grey')
startMsgRect = startMsg.get_rect(center=(S.SCREEN_WIDTH/2, S.START_MSG_Y))

# Timer
obstacleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleTimer, S.OBSTACLE_TIMER_INTERVAL)
idleFrameTimer = 0

while True:
    for event in pygame.event.get():
        # Player quit
        if event.type == pygame.QUIT:
            updateHighscore()
            with open ('highscore.json', 'w') as highscoreFile:
                json.dump(highscoreData, highscoreFile)
            pygame.quit()
            exit()
        # Player pause
        if event.type == pygame.KEYDOWN:
            # Update game state only if pause is valid
            if event.key == pygame.K_ESCAPE and gameActive:
                gamePaused = not gamePaused
                # Start pause timer
                if gameActive and gamePaused:
                    overlayDrawn = False
                    pauseTime = pygame.time.get_ticks()
                    pygame.mixer.pause()
                # Get pause duration to recalibrate score
                elif gameActive and not gamePaused:
                    pauseDuration = pygame.time.get_ticks() - pauseTime
                    startTime += int(pauseDuration / 1000)
                    pygame.mixer.unpause()
        # Obstacle spawn
        if gameActive and not gamePaused:
            if event.type == obstacleTimer:
                selectedType, selectedFrames = choice([('fly', flyFrames), ('mouse', mouseFrames), ('mouse', mouseFrames), ('other', flyFrames),])
                obstacleGroup.add(Obstacle(selectedType, selectedFrames))
        # Restart game
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gameActive = True
                startTime = int(pygame.time.get_ticks() / 1000)
                updateHighscore()
    # Ongoing game
    if gameActive and not gamePaused:
        drawBackground()

        # Get and display the player's current score
        score = displayScore()

        # Player update
        player.draw(screen)
        player.update() 

        # Obstacle update
        obstacleGroup.draw(screen)
        obstacleGroup.update()

        # Collision update (end if detected)
        gameActive = spriteCollision()
    # Paused game
    elif gamePaused:
        if not overlayDrawn:
            drawPauseScreen()
            overlayDrawn = True
    # Game over
    else:
        screen.fill('black')
        idleFrameTimer = drawIdleScreen(playerIdleFrames, idleFrameTimer)
        screen.blit(gameName, gameNameRect)
        screen.blit(gameSubName, gameSubRect)
        screen.blit(startMsg, startMsgRect)
        # At least one game played during this session
        if score != 0:
            if score > highscoreData['highscore']:
                displayFinalScore(f'Your score: {score} (new high score!)', gameFontSm, (S.SCREEN_WIDTH/2, S.FINAL_SCORE_Y))
            else:
                displayFinalScore(f'Your score: {score} | Highscore: {highscoreData["highscore"]}', gameFontSm, (S.SCREEN_WIDTH/2, S.FINAL_SCORE_Y))
        elif highscoreData['highscore'] > 0:
            displayFinalScore(f'Highscore: {highscoreData["highscore"]}', gameFontSm, (S.SCREEN_WIDTH/2, S.FINAL_SCORE_Y))

    pygame.display.update()
    clock.tick(60)
