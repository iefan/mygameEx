# -*- coding: utf-8 -*-
import pygame, sys
from pygame.locals import *

pygame.init()

# FPS = 30
# fpsClock = pygame.time.Clock()
#设置颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

blockWidth = 40

curSurface = pygame.display.set_mode((600, 560), 0, 32)
pygame.display.set_caption("Puzzle")

poems = ['春眠不觉晓，','处处闻啼鸟。','夜来风雨声，','花落知多少。']
fontObj = pygame.font.Font('simsunb.ttf', 32)
fontObj = pygame.font.SysFont("simhei", 50)
headTextObj = fontObj.render("春 晓", True, GREEN, BLUE)
headRectObj = headTextObj.get_rect()
headRectObj.center = (300, 50)

lstfont = []
count = 2
for i in poems:
    textSurfaceObj = fontObj.render(i, True, BLUE, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (300, 100*count)
    lstfont.append([textSurfaceObj, textRectObj])
    count += 1


# soundObj = pygame.mixer.Sound('sound/secosmic_lo.wav')
# soundObj.play()


# catImg = pygame.image.load("image/cat.png")
# catImg2 = pygame.image.load("image/cat2.png")
# catImg_right = pygame.transform.smoothscale(catImg, (100,80))
# catImg_right2 = pygame.transform.smoothscale(catImg2, (100,80))
# catImg_left = pygame.transform.flip(catImg_right, 1, 0)
# catImg_left2 = pygame.transform.flip(catImg_right2, 1, 0)

# catx = 10
# caty = 100
# direction = 'right'

# for i in range(10):
#     for j in range(10):
#         tmpblockpos = (10+i*blockWidth, 10+j*blockWidth)
#         pygame.draw.rect(curSurface, BLUE, (10+i*blockWidth,10+j*blockWidth, blockWidth, blockWidth))

# curSurface.fill(WHITE)
# for i in range(10):
#     for j in range(10):
#         tmpblockpos = (10+i*blockWidth, 10+j*blockWidth)
#         pygame.draw.rect(curSurface, BLUE, (70+i*(blockWidth+5),90+j*(blockWidth+5), blockWidth, blockWidth))

# curSurface.fill(WHITE)
# flag = True
while True:
    curSurface.fill(WHITE)
    curSurface.blit(textSurfaceObj, textRectObj)
    for iobj in lstfont:
        curSurface.blit(iobj[0], iobj[1])

    curSurface.blit(headTextObj, headRectObj)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    # fpsClock.tick(FPS)