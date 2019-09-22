# -*- coding: utf-8 -*-
import pygame, sys, random
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
NAVYBLUE = ( 60, 60, 100)

blockWidth = 45

curSurface = pygame.display.set_mode((600, 560), 0, 32)
pygame.display.set_caption("迷宫")

# fontObj = pygame.font.Font('simsunb.ttf', 32)
fontObj = pygame.font.SysFont("simhei", 50)
headTextObj = fontObj.render("迷宫", True, GREEN, WHITE)
headRectObj = headTextObj.get_rect()
headRectObj.center = (300, 50)

lstBlockRect = []
def drawBackGround():
    curSurface.fill(NAVYBLUE)
    for i in range(6):
        for j in range(6):
            lstBlockRect[i][j] = (70+i*(blockWidth+30),90+j*(blockWidth+30), blockWidth, blockWidth)
            pygame.draw.rect(curSurface, WHITE, (70+i*(blockWidth+30),90+j*(blockWidth+30), blockWidth, blockWidth))
    curSurface.blit(headTextObj, headRectObj)
# curSurface.fill(WHITE)
# flag = True

lstIcon = []
def loadIcon():
    for i in range(1, 19):
        iconname = 'image/fruit'+str(i) + '.png'
        tmpimg = pygame.image.load(iconname)
        tmpimg = pygame.transform.smoothscale(tmpimg, (40,40))
        lstIcon.append(tmpimg)
        lstIcon.append(tmpimg)

loadIcon()
random.shuffle(lstIcon)

# print(lstIcon, len(lstIcon))
def drawIcon():
    for i in range(6):
        for j in range(6):
            pygame.draw.rect(curSurface, NAVYBLUE, (70+i*(blockWidth+30),90+j*(blockWidth+30), blockWidth, blockWidth))
            curSurface.blit(lstIcon[i*6+j], (70+i*(blockWidth+30),90+j*(blockWidth+30), blockWidth, blockWidth))

while True:
    drawBackGround()
    drawIcon()
    # curSurface.fill(WHITE)
    # curSurface.blit(textSurfaceObj, textRectObj)
    # for iobj in lstfont:
    #     curSurface.blit(iobj[0], iobj[1])

    # curSurface.blit(headTextObj, headRectObj)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    # fpsClock.tick(FPS)