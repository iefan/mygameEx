# -*- coding: utf-8 -*-
import pygame, sys, random
from pygame.locals import *
import os
x = 100
y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y) #设置窗口起始位置

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
headTextObj = fontObj.render("迷宫", True, WHITE, NAVYBLUE)
headRectObj = headTextObj.get_rect()
headRectObj.center = (300, 50)

m = 6
n = 6
lstBlockRect = [[0 for i in range(m)] for j in range(n)]
lstBlockFlag = [[0 for i in range(m)] for j in range(n)]
def generatePos():
    for i in range(m):
        for j in range(n):
            lstBlockRect[i][j] = (70+i*(blockWidth+30),90+j*(blockWidth+30), blockWidth, blockWidth)

generatePos() #生成所有图标的位置数据
## print(lstBlockRect)

# 将图标加载到全局列表中
lstIcon = []
def loadIcon():
    for i in range(1, 19):
        iconname = 'image/fruit'+str(i) + '.png'
        tmpimg = pygame.image.load(iconname)
        tmpimg = pygame.transform.smoothscale(tmpimg, (40,40))
        lstIcon.append(tmpimg)
        lstIcon.append(tmpimg)

loadIcon()
random.shuffle(lstIcon)#将图标排列随机化

# 根据用户点击鼠标位置查找到相应的图标
def findBlockByPos(mouse_x, mouse_y):
    for i in range(m):
        for j in range(n):
            if mouse_x > lstBlockRect[i][j][0] and mouse_x <= lstBlockRect[i][j][0] + blockWidth:
                if mouse_y > lstBlockRect[i][j][1] and mouse_y <= lstBlockRect[i][j][1] + blockWidth:
                    # print("pos", i, j)
                    return (i,j)
    return(-1,-1)

#绘制背景
def drawBackGround():
    curSurface.fill(NAVYBLUE)
    for i in range(m):
        for j in range(n):
            if lstBlockFlag[i][j] == 0:
                pygame.draw.rect(curSurface, WHITE, lstBlockRect[i][j])
            else:
                pygame.draw.rect(curSurface, NAVYBLUE, (70+i*(blockWidth+30),90+j*(blockWidth+30), blockWidth, blockWidth))
                curSurface.blit(lstIcon[i*6+j], (70+i*(blockWidth+30),90+j*(blockWidth+30), blockWidth, blockWidth))
    curSurface.blit(headTextObj, headRectObj)

# 根据位置绘制图标
def drawIcon(indx_x=-1, indx_y=-1):
    if indx_x == -1 and indx_y == -1:
        for i in range(6):
            for j in range(6):
                pygame.draw.rect(curSurface, NAVYBLUE, (70+i*(blockWidth+30),90+j*(blockWidth+30), blockWidth, blockWidth))
                curSurface.blit(lstIcon[i*6+j], (70+i*(blockWidth+30),90+j*(blockWidth+30), blockWidth, blockWidth))
    else:
        i = indx_x
        j = indx_y

        pygame.draw.rect(curSurface, NAVYBLUE, (70+i*(blockWidth+30),90+j*(blockWidth+30), blockWidth, blockWidth))
        curSurface.blit(lstIcon[i*6+j], (70+i*(blockWidth+30),90+j*(blockWidth+30), blockWidth, blockWidth))

for i in range(m*n):
    for j in range(m*n):
        if i!=j and lstIcon[i] == lstIcon[j]:
            print(i,j)

while True:
    drawBackGround()
    mouse_x,mouse_y = -1,-1
    # drawIcon() #绘制所有图标
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
            print(event.key, chr(event.key), pygame.key.get_mods())
            if event.key in (K_h, K_e, K_l, K_o, K_w, K_r, K_d):
                if pygame.key.get_mods() in (1, 8192):
                    print("你输入的是：", chr(event.key).upper())
                else:
                    print("你输入的是：", chr(event.key))
    
    curIcon = findBlockByPos(mouse_x, mouse_y)
    if curIcon != (-1,-1):
        drawIcon(curIcon[0], curIcon[1])
        lstBlockFlag[curIcon[0]][curIcon[1]] = 1
        # pygame.time.wait(1000)
    pygame.display.update()
    # fpsClock.tick(FPS)
