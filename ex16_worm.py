# -*- coding: utf-8 -*-
import pygame, sys, random, math
from pygame.locals import *
import os, string

pos_x = 100
pos_y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (pos_x,pos_y) #设置窗口起始位置

pygame.init()

FPS = 20
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
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20

curSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption("贪食蛇游戏") 
TimerEvent1 = pygame.USEREVENT
pygame.time.set_timer(TimerEvent1, 0)

g_Fontsize = 60
g_fontObj = pygame.font.SysFont("simhei", g_Fontsize)
g_titleSurf2 = g_fontObj.render("抖动旋转", True, GREEN, NAVYBLUE)

g_zoom_flag = 1
g_scale = 1.2

def drawGrid():
    for i in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(curSurface, DARKGRAY, (i,0), (i, WINDOWHEIGHT))
    for j in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(curSurface, DARKGRAY, (0,j), (WINDOWWIDTH, j))

def terminate():
    pygame.quit()
    sys.exit()

def drawPressKeyMsg():
    basicFont = pygame.font.SysFont("simhei", 18)
    pressKeySurf = basicFont.render("按任意键继续...", True, YELLOW, BLACK)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH-140, WINDOWHEIGHT-20)
    curSurface.blit(pressKeySurf, pressKeyRect)

def checkUserEvent():
    global g_Fontsize, g_fontObj, g_titleSurf2
    userEvents = pygame.event.get(TimerEvent1)
    if len(userEvents) == 0:
        return None
    # if g_Fontsize > 30:
    #     g_Fontsize -= 2
    # else:
    #     g_Fontsize = 60

    if g_zoom_flag == 1:
        if g_Fontsize > 30 : 
            g_Fontsize -= 2            
    else:
        if g_Fontsize < 60 : 
            g_Fontsize += 2
    
    g_fontObj = pygame.font.SysFont("simhei", g_Fontsize)
    g_titleSurf2 = g_fontObj.render("抖动旋转", True, GREEN, YELLOW)


def checkForKeyPress():
    if len(pygame.event.get(QUIT))>0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    print(keyUpEvents)
    return keyUpEvents[0].key

def showStartScreen():
    # Once the font is created the size cannot be changed.
    global  g_titleSurf1, g_titleSurf2, g_zoom_flag, g_scale
    fontObj = pygame.font.SysFont("simhei", 80)
    titleSurf1 = fontObj.render("贪食蛇游戏", True, WHITE, BLACK)

    pygame.time.set_timer(TimerEvent1, 100)
    
    degrees1 = 0

    while True:
        curSurface.fill(BLACK)
        rotatedSurf1 = pygame.transform.rotozoom(titleSurf1, degrees1, g_scale)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH//2, WINDOWHEIGHT // 2) 
        curSurface.blit(rotatedSurf1, rotatedRect1) 

        
        drawPressKeyMsg()

        checkUserEvent()
        
        drawGrid()
        if checkForKeyPress():
            pygame.event.get()
            #continue
            return
                               
        pygame.display.update()
        fpsClock.tick(FPS)
        
        if g_zoom_flag == 1:
            if g_scale > 0.2 : 
                g_scale -= 0.01
                degrees1 += 3
            else:
                g_zoom_flag = 0               
        else:
            if g_scale < 1.2 :
                g_scale += 0.01
                degrees1 -= 3
            else:
                g_zoom_flag = 1
            


def main():
    showStartScreen()

if __name__ == "__main__":
    main()
