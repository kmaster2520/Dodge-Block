#- Dodge Block
# By Sathvik Kadaveru

# must have pygame and python3 to play

import pygame,sys
from pygame.locals import *
from random import *
import time

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
BLUE  = (  0,   0, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
ENEMYCOLOR = RED
PLAYERCOLOR = BLUE
BLOCKWIDTH = 20
BLOCKHEIGHT = BLOCKWIDTH
DX = 14
DY = DX

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([BLOCKWIDTH, BLOCKHEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = dx
        self.dy = dy
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

screen_w = 700
screen_h = 500

pygame.init()
mainClock = pygame.time.Clock()
window = pygame.display.set_mode((screen_w, screen_h+30), 0, 32)
pygame.display.set_caption('Dodge Block')

myFont = pygame.font.SysFont("Courier",14)
myFont72 = pygame.font.SysFont("Courier",54)

activeblocks = pygame.sprite.Group()
allsprites = pygame.sprite.Group()


gameOver = True

score = 0
slowdown = 200
slowDisabled = False
isSlow = False
START_X = screen_w//2
START_Y = screen_h//2
SPEED = 10
Player = Block(START_X, START_Y, 0, 0, PLAYERCOLOR)
allsprites.add(Player)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    window.fill(BLACK)
    keys = pygame.key.get_pressed()

    if gameOver:
        titleText = myFont72.render('Dodge Block', 1, WHITE)
        textRect = titleText.get_rect()
        textRect.centerx = screen_w//2
        textRect.centery = screen_h//4
        window.blit(titleText, textRect)
        #
        titleText = myFont.render('Press Return to Continue', 1, WHITE)
        textRect = titleText.get_rect()
        textRect.centerx = screen_w//2
        textRect.centery = screen_h//2
        window.blit(titleText, textRect)
        #
        titleText = myFont72.render('Your Score: ' + '%3d'%score, 1, WHITE)
        textRect = titleText.get_rect()
        textRect.centerx = screen_w//2
        textRect.centery = 3*screen_h//4
        window.blit(titleText, textRect)
        #
        if keys[K_RETURN]:
            gameOver=False
            activeblocks.empty()
            allsprites.empty()
            Player = Block(START_X, START_Y, 0, 0, PLAYERCOLOR)
            allsprites.add(Player)
            score = 0
            slowdown = 200
            slowDisabled = False

    elif not gameOver:
        if keys[K_LEFT] and Player.rect.x > -BLOCKWIDTH:
            Player.rect.x -= SPEED
        if keys[K_RIGHT] and Player.rect.x < screen_w + BLOCKWIDTH:
            Player.rect.x += SPEED
        if keys[K_UP] and Player.rect.y > -BLOCKHEIGHT:
            Player.rect.y -= SPEED
        if keys[K_DOWN] and Player.rect.y < screen_h + BLOCKHEIGHT:
            Player.rect.y += SPEED

        isSlow = keys[K_SPACE] and not slowDisabled
        if isSlow:
            slowdown -= 6
            slowdown = max(slowdown, 0)
            if slowdown <= 0:
                isSlow = False
                slowDisabled = True

        elif slowdown < 200:
            slowdown += 2
            slowdown = min(slowdown, 200)
            isSlow = False
            if slowdown >= 200:
                slowDisabled = False


        if random() < 0.13 and not isSlow:
            option = randint(1, 4)
            if option == 1:
                newBlock = Block(int(screen_w * random()), 0,
                                 0, DY, ENEMYCOLOR)
            elif option == 2:
                newBlock = Block(int(screen_w * random()), screen_h,
                                 0, -DY, ENEMYCOLOR)
            elif option == 3:
                newBlock = Block(0, int(screen_h * random()),
                                 DX, 0, ENEMYCOLOR)
            else:
                newBlock = Block(screen_w, int(screen_h * random()),
                                 -DX, 0, ENEMYCOLOR)

            activeblocks.add(newBlock)
            allsprites.add(newBlock)

        if not isSlow:
            activeblocks.update()
        allsprites.draw(window)

        for block in activeblocks:
            if not (-2*BLOCKHEIGHT < block.rect.y < screen_h+BLOCKHEIGHT and
                    -2*BLOCKWIDTH< block.rect.x < screen_w+BLOCKWIDTH):
                activeblocks.remove(block)
                allsprites.remove(block)
                score += 1
                if score % 50 == 0:
                    DX += 2
                    DY += 2


        pygame.draw.rect(window, BLACK, (0, screen_h, screen_w, 30), 0)

        scoreText = myFont.render('Your Score: ' + '%3d'%score, 1, WHITE)
        window.blit(scoreText, (5, screen_h + 5))

        slowText = myFont.render('Slowdown (Press Space)', 1, WHITE)
        window.blit(slowText, (screen_w//2 - 180, screen_h + 5))
        if not slowDisabled:
            pygame.draw.rect(window, GREEN, (screen_w//2, screen_h + 5, slowdown//2, 10))
        else:
            pygame.draw.rect(window, RED, (screen_w//2, screen_h + 5, slowdown//2, 10))

        if pygame.sprite.spritecollide(Player, activeblocks, False):
            gameOver=True

        timeText=myFont.render(time.strftime('Time %H:%M  (%Z)'),True,WHITE)
        window.blit(timeText, (screen_w*3//4, screen_h + 5))



    pygame.display.update()
    mainClock.tick(30)


