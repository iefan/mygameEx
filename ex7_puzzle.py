# -*- coding: utf-8 -*-
import pygame, sys, random
from pygame.locals import *
x = 100
y = 100
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

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

m = 6
n = 6
lstBlockRect = [[0 for i in range(m)] for j in range(n)]
def generatePos():
    for i in range(m):
        for j in range(n):
            lstBlockRect[i][j] = (70+i*(blockWidth+30),90+j*(blockWidth+30), blockWidth, blockWidth)

generatePos()
## print(lstBlockRect)

def findBlockByPos(mouse_x, mouse_y):
    for i in range(m):
        for j in range(n):
            if mouse_x > lstBlockRect[i][j][0] and mouse_x <= lstBlockRect[i][j][0] + blockWidth:
                if mouse_y > lstBlockRect[i][j][1] and mouse_y <= lstBlockRect[i][j][1] + blockWidth:
                    print("pos", i, j)

def drawBackGround():
    curSurface.fill(NAVYBLUE)
    for i in range(m):
        for j in range(n):
            pygame.draw.rect(curSurface, WHITE, lstBlockRect[i][j])
    curSurface.blit(headTextObj, headRectObj)

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
    mouse_x,mouse_y = -1,-1
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
        elif event.type == MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            # print(mouse_x, mouse_y)
        elif event.type == KEYUP:
            if event.key in (K_h, K_e, K_l, K_o, K_w, K_r, K_d):
                print(event.key, chr(event.key))
    
    findBlockByPos(mouse_x, mouse_y)
    pygame.display.update()
    # fpsClock.tick(FPS)
