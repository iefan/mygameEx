# -*- coding: utf-8 -*-
import pygame, sys, random
from pygame.locals import *
import os
pos_x = 100
pos_y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (pos_x,pos_y) #设置窗口起始位置

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
YELLOW = (255, 255,0)


blockWidth = 45
g_ClickCount = -1
g_TotalSecond = 0
first_ClickIcon = [0,0]
second_ClickIcon = [0,0]

curSurface = pygame.display.set_mode((630, 560), 0, 32)
pygame.display.set_caption("迷宫")

# fontObj = pygame.font.Font('simsunb.ttf', 32)
fontObj = pygame.font.SysFont("simhei", 50)
headTextObj = fontObj.render("迷宫", True, WHITE, NAVYBLUE)
headRectObj = headTextObj.get_rect()
headRectObj.center = (300, 50)

infoFontObj = pygame.font.SysFont("simhei", 16)
infoTextObj = infoFontObj.render("点击次数：", True, YELLOW, NAVYBLUE)
infoRectObj = infoTextObj.get_rect()
infoRectObj.center = (580, 100)
infoTextObj2 = infoFontObj.render("0 次", True, YELLOW, NAVYBLUE)
infoRectObj2 = infoTextObj2.get_rect()
infoRectObj2.center = (580, 130)

infoTextObj3 = infoFontObj.render("计  时", True, YELLOW, NAVYBLUE)
infoRectObj3 = infoTextObj3.get_rect()
infoRectObj3.center = (580, 200)

infoTextObj4 = infoFontObj.render("0 秒", True, YELLOW, NAVYBLUE)
infoRectObj4 = infoTextObj4.get_rect()
infoRectObj4.center = (580, 230)

infoHelpText = infoFontObj.render("按g重新开始", True, YELLOW, NAVYBLUE)
infoHelpRect = infoHelpText.get_rect()
infoHelpRect.center = (580, 300)


m = 6
n = 6
lstBlockRect = [[0 for i in range(m)] for j in range(n)]
lstBlockFlag = [[1 for i in range(m)] for j in range(n)]
lstBlockFlag_OVER = [[1 for i in range(m)] for j in range(n)]
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
    curSurface.blit(infoTextObj, infoRectObj)
    curSurface.blit(infoTextObj2, infoRectObj2)
    curSurface.blit(infoTextObj3, infoRectObj3)
    curSurface.blit(infoTextObj4, infoRectObj4)
    curSurface.blit(infoHelpText, infoHelpRect)

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
            print(i,j, '===>', (i%6+1, i//6+1), (j%6+1, j//6+1))

DISPFIRST = pygame.USEREVENT #创建自定义事件，第一次全部显示供用户记忆
pygame.time.set_timer(DISPFIRST, 5000)

DISPINFOTEXT = pygame.USEREVENT+1 #创建自定义事件，计时
pygame.time.set_timer(DISPINFOTEXT, 0)


# lstBlockFlag = [[1 for i in range(m)] for j in range(n)]

while True:
    drawBackGround()
    mouse_x,mouse_y = -1,-1
    
    if g_ClickCount%2==0 and second_ClickIcon[0] != first_ClickIcon[0]:
        # print(first_ClickIcon, second_ClickIcon)
        pygame.time.wait(300)
        lastIcon = first_ClickIcon[1]
        thisIcon = second_ClickIcon[1]
        lstBlockFlag[lastIcon[0]][lastIcon[1]] = 0
        lstBlockFlag[thisIcon[0]][thisIcon[1]] = 0
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
        elif event.type == DISPFIRST:
            lstBlockFlag = [[0 for i in range(m)] for j in range(n)]
            g_ClickCount = 0
            pygame.time.set_timer(DISPFIRST, 0)
            pygame.time.set_timer(DISPINFOTEXT, 1000)

        elif event.type == DISPINFOTEXT:
            g_TotalSecond += 1
            infoTextObj4 = infoFontObj.render(str(g_TotalSecond)+"秒", True, YELLOW, NAVYBLUE)
            infoRectObj4 = infoTextObj4.get_rect()
            infoRectObj4.center = (580, 230)
            if lstBlockFlag == lstBlockFlag_OVER:
                pygame.time.set_timer(DISPINFOTEXT, 0) #全部选完关闭计时
            # print(g_TotalSecond)

        elif event.type == KEYUP:
            print(event.key, chr(event.key)=='g', pygame.key.get_mods())
            if chr(event.key) == 'g': #重新开始
                g_ClickCount = 0
                g_TotalSecond = 0
                first_ClickIcon = [0,0]
                second_ClickIcon = [0,0]
                lstBlockFlag = [[0 for i in range(m)] for j in range(n)]
                infoTextObj2 = infoFontObj.render("0次", True, YELLOW, NAVYBLUE)
                infoRectObj2 = infoTextObj2.get_rect()
                infoRectObj2.center = (580, 130)
               
    
    curIcon = findBlockByPos(mouse_x, mouse_y)
    if curIcon != (-1,-1) and  lstBlockFlag != lstBlockFlag_OVER:
        #显示点击次数
        g_ClickCount += 1
        infoTextObj2 = infoFontObj.render(str(g_ClickCount)+"次", True, YELLOW, NAVYBLUE)
        infoRectObj2 = infoTextObj2.get_rect()
        infoRectObj2.center = (580, 130)

        # 修改被击点的图标标志
        lstBlockFlag[curIcon[0]][curIcon[1]] = 1
        indx_icon = curIcon[0]*n+curIcon[1]
        if g_ClickCount % 2 == 1: 
            first_ClickIcon = [lstIcon[indx_icon], curIcon]
        else:
            second_ClickIcon = [lstIcon[indx_icon], curIcon]
            
    pygame.display.update()
    # fpsClock.tick(FPS)
