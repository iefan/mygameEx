# -*- coding: utf-8 -*-
import pygame, sys, random, math
from pygame.locals import *
import os, string

pos_x = 100
pos_y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (pos_x,pos_y) #设置窗口起始位置

pygame.init()

FPS = 15
fpsClock = pygame.time.Clock()
#设置颜色
BLACK = (0, 0, 0)
BLUE  = (0, 0, 255)
NAVYBLUE = ( 60, 60, 100)
YELLOW_D = (120, 120,0)
WHITE_D = (128, 128, 128)
RED_D   = (120, 0, 0)
GREEN_D = (0, 120, 0)
YELLOW = (255, 255,0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 200, 0)
MAROON = (200,0,200)
GRAY = (100, 100, 100)

curSurface = pygame.display.set_mode((630, 560), 0, 32)
pygame.display.set_caption("字幕演示")

# startfontObj = pygame.font.Font('simsunb.ttf', 32)
numberFontObj = pygame.font.SysFont("simhei", 40)
startfontObj = pygame.font.SysFont("simhei", 30)

fontObj = pygame.font.SysFont("simhei", 50)
headTextObj = fontObj.render("字幕演示", True, WHITE, NAVYBLUE)
headRectObj = headTextObj.get_rect()
headRectObj.center = (300, 50)


startTextObj = startfontObj.render("开始", True, WHITE, NAVYBLUE)
startRectObj = startTextObj.get_rect()
startRectObj.left = 530
startRectObj.top = 460


g_BGRECT = []
g_FONTRECT = []
g_FONTRECT2 = []
g_GAMEOVER = True
g_StrAlpha = ''
g_Count = 0
g_ALPHANUMS = [10,15,20,26]

def genRectPos():
    blockLeft = 50
    blockTop = 140
    blockWidth = 100
    for i in range(4):
        tmprect = pygame.Rect(blockLeft+i*(blockWidth+10), blockTop, blockWidth, blockWidth)
        tmpFontText = fontObj.render(".", True, WHITE, BLACK)
        tmpFontRect = tmpFontText.get_rect()
        tmpFontRect.center = tmprect.center
        g_BGRECT.append(tmprect)
        g_FONTRECT.append([tmpFontText, tmpFontRect])

    for i in range(4):
        tmprect = pygame.Rect(blockLeft+i*(blockWidth+10), blockTop+blockWidth+50, blockWidth, blockWidth)
        tmpFontText = fontObj.render(".", True, WHITE, BLACK)
        tmpFontRect = tmpFontText.get_rect()
        tmpFontRect.center = tmprect.center
        g_BGRECT.append(tmprect)
        g_FONTRECT2.append([tmpFontText, tmpFontRect])

    left = 30
    top = 90
    width = 480
    height = 430
    rect = pygame.Rect(left, top, width, height)
    g_BGRECT.append(rect)
    
#绘制背景
def drawBackGround():
    global g_FONTRECT, g_GAMEOVER
    # print(g_FONTRECT)
    # print(nameRect)
    curSurface.fill(NAVYBLUE)
    pygame.draw.rect(curSurface, YELLOW, g_BGRECT[-1],  2)

    # if g_GAMEOVER == False:
    #     print(len(g_BGRECT), g_FONTRECT[0])
    for i in range(4):
        pygame.draw.rect(curSurface, BLACK, g_BGRECT[i])
        curSurface.blit(g_FONTRECT[i][0], g_FONTRECT[i][1])

    for i in range(4):
        pygame.draw.rect(curSurface, BLACK, g_BGRECT[i+4])
        curSurface.blit(g_FONTRECT2[i][0], g_FONTRECT2[i][1])

    curSurface.blit(headTextObj, headRectObj)
    curSurface.blit(startTextObj, startRectObj)


def calcClickFlag(pos):
    global g_GAMEOVER
    if g_GAMEOVER:
        if startRectObj.collidepoint(pos):
            StartGameSet(1)
        return


def changeAlpha():
    global g_FONTRECT, g_StrAlpha, g_Count, g_GAMEOVER
    # ialpha = g_StrAlpha[g_Count]
    g_Count += 1
    g_FONTRECT.clear()
    g_FONTRECT2.clear()
    str_DispWords = '中国机长'
    str_DispWords2 = '刘传健！'

    for item in g_BGRECT[:4]:
        random.shuffle(g_StrAlpha)
        ialpha = g_StrAlpha[g_Count]
        if g_Count >= g_ALPHANUMS[len(g_FONTRECT)]:
            tmpFontText = fontObj.render(str_DispWords[len(g_FONTRECT)], True, WHITE, BLACK)
        else:
            tmpFontText = fontObj.render(ialpha, True, WHITE, BLACK)
        # tmpFontText = fontObj.render(ialpha, True, WHITE, BLACK)
        tmpFontRect = tmpFontText.get_rect()
        tmpFontRect.center = item.center
        g_FONTRECT.append([tmpFontText, tmpFontRect])

    for item in g_BGRECT[4:8]:
        random.shuffle(g_StrAlpha)
        ialpha = g_StrAlpha[g_Count]
        tmpFontText = fontObj.render(ialpha, True, YELLOW, BLACK)
        tmpFontRect = tmpFontText.get_rect()
        tmpFontRect.center = item.center
        g_FONTRECT2.append([tmpFontText, tmpFontRect])

    if g_Count == 50:
        g_GAMEOVER = True
        g_FONTRECT2.clear()
        icount = 0
        for item in g_BGRECT[4:8]:
            tmpFontText = fontObj.render(str_DispWords2[icount], True, YELLOW, BLACK)
            tmpFontRect = tmpFontText.get_rect()
            tmpFontRect.center = item.center
            g_FONTRECT2.append([tmpFontText, tmpFontRect])
            icount += 1

def StartGameSet(flag_qishi=0): 
    global g_BGRECT, g_StrAlpha, g_Count, g_GAMEOVER, g_ALPHANUMS
    g_StrAlpha = list(string.ascii_uppercase*2)
    g_ALPHANUMS = [15,25,35,45]
    g_Count = 0
    g_GAMEOVER = True
    g_BGRECT = []
    genRectPos()   
    if flag_qishi == 1:
        g_GAMEOVER = False 
    

StartGameSet()

while True:
    drawBackGround()
    if g_GAMEOVER==False:
        changeAlpha()
  
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            calcClickFlag(event.pos)
        
        elif event.type == KEYUP:
            print(event.key, chr(event.key)=='↑', pygame.key.get_mods())
                           
    pygame.display.update()
    fpsClock.tick(FPS)