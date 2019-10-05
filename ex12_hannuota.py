# -*- coding: utf-8 -*-
import pygame, sys, random, math
from pygame.locals import *
import os
import pygame_textinput
import pygame.gfxdraw

pos_x = 100
pos_y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (pos_x,pos_y) #设置窗口起始位置

pygame.init()

FPS = 50
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

blockWidth =100 
# g_ClickCount = -1
g_TotalSecond = 0
g_TotalPieNums = 4

g_USERNAME = "psy"


textinput = pygame_textinput.TextInput(initial_string=g_USERNAME, font_size=24, text_color=WHITE, font_family="simhei")

curSurface = pygame.display.set_mode((630, 560), 0, 32)
pygame.display.set_caption("汉诺塔游戏")

# fontObj = pygame.font.Font('simsunb.ttf', 32)
numberFontObj = pygame.font.SysFont("simhei", 36)
resultFontObj = pygame.font.SysFont("simhei", 22)

fontObj = pygame.font.SysFont("simhei", 50)
headTextObj = fontObj.render("汉诺塔游戏", True, WHITE, NAVYBLUE)
headRectObj = headTextObj.get_rect()
headRectObj.center = (300, 50)

infoFontObj = pygame.font.SysFont("simhei", 16)
# infoTextObj = infoFontObj.render("成绩", True, YELLOW, NAVYBLUE)
# infoRectObj = infoTextObj.get_rect()
# infoRectObj.center = (580, 120)
# infoTextObj2 = infoFontObj.render("0步", True, YELLOW, NAVYBLUE)
# infoRectObj2 = infoTextObj2.get_rect()
# infoRectObj2.center = (580, 150)

infoAreaTop = 100
infoAreaLeft = 530
infoTextObj3 = infoFontObj.render("计  时", True, YELLOW, NAVYBLUE)
infoRectObj3 = infoTextObj3.get_rect()
infoRectObj3.top = infoAreaTop + 10
infoRectObj3.left = infoAreaLeft

infoTextObj4 = infoFontObj.render("0秒", True, YELLOW, NAVYBLUE)
infoRectObj4 = infoTextObj4.get_rect()
infoRectObj4.top = infoRectObj3.bottom + 10
infoRectObj4.left = infoAreaLeft
# infoRectObj4.center = (580, 230)

infoHelpText = infoFontObj.render("按回车开始", True, YELLOW, NAVYBLUE)
infoHelpRect = infoHelpText.get_rect()
infoHelpRect.top = infoRectObj4.bottom + 20
infoHelpRect.left = infoAreaLeft
# infoHelpRect.center = (575, 270)

nameText = infoFontObj.render("玩家：", True, WHITE, NAVYBLUE)
nameRect = nameText.get_rect()
nameRect.top = infoHelpRect.bottom + 30
nameRect.left = infoAreaLeft
# nameRect.center = (570, 320)

rankTmpText = infoFontObj.render("排名", True, YELLOW, NAVYBLUE)
rankTmpRect = rankTmpText.get_rect()
rankTmpRect.left = infoAreaLeft
rankTmpRect.top = nameRect.bottom + 80

Level3Text = infoFontObj.render("三阶", True, WHITE, NAVYBLUE)
Level3Rect = Level3Text.get_rect()
Level3Rect.top = 440
Level3Rect.left = infoAreaLeft

Level4Text = infoFontObj.render("四阶", True, WHITE, NAVYBLUE)
Level4Rect = Level4Text.get_rect()
Level4Rect.top = Level3Rect.bottom+10
Level4Rect.left = infoAreaLeft

Level5Text = infoFontObj.render("五阶", True, WHITE, NAVYBLUE)
Level5Rect = Level5Text.get_rect()
Level5Rect.top = Level4Rect.bottom+10
Level5Rect.left = infoAreaLeft

lstRankInfo = []
lstRankNameAndTime = {'3':[], '4':[], '5':[]}
def getRankInfo(flag = "read"):
    global lstRankInfo, lstRankNameAndTime
    if flag == 'read':
        lstRankNameAndTime = {'3':[], '4':[], '5':[]}
        if os.path.exists(r'rankHannuota.dat'):
            with open(r'rankHannuota.dat', encoding='utf-8' ) as f:
                icount = 0
                
                for irank in f.readlines():
                    
                    irank = irank.strip()
                    if len(irank) == 0:
                        break
                    tmplevel,tmpsecond, tmpname = irank.split(',')
                    # print(tmplevel, type(g_TotalPieNums))
                    lstRankNameAndTime[tmplevel].append([int(tmpsecond), tmpname])
                
                lstRankInfo = []
                for ikey in lstRankNameAndTime:
                    if int(ikey) == g_TotalPieNums:
                        lstRankNameAndTime[ikey].sort()
                        for iitem in lstRankNameAndTime[ikey][:3]:
                            icount += 1
                            rankTmpText = infoFontObj.render(iitem[1]+":"+str(iitem[0])+"秒", True, YELLOW, NAVYBLUE)
                            rankTmpRect = rankTmpText.get_rect()
                            rankTmpRect.left = infoAreaLeft
                            rankTmpRect.top = nameRect.bottom + 80 +icount*25
                            # rankTmpRect.center = (570, 400+icount*30)
                            lstRankInfo.append([rankTmpText, rankTmpRect])
                    # print(lstRankNameAndTime)
              
    elif flag=="write":
        lstRankNameAndTime[str(g_TotalPieNums)].append([g_TotalSecond-1, g_USERNAME])
        lstRankNameAndTime[str(g_TotalPieNums)].sort()
        # print(lstRankNameAndTime,'write')
        rankInfoStr = ""
        for ikey in lstRankNameAndTime:
            for item in lstRankNameAndTime[ikey]:
                rankInfoStr += ikey + "," + str(item[0]) + "," + item[1] + '\n'
        with open(r'rankHannuota.dat', 'w', encoding='utf-8' ) as f:
            f.write(rankInfoStr)

        getRankInfo()


def genRectPos():
    # global g_NumberRect
    dipanWidth = 120
    dipanHeight = 40
    dipanLeft = 40
    dipanTop = 430

    zhuziWidth = 5
    zhuziHeight = 220
    # zhuziLeft = dipanLeft +(dipanWidth - zhuziWidth)//2
    zhuziTop = dipanTop - zhuziHeight

    lap = 10
    pieWidth = dipanWidth - lap*2
    pieHeight = 20

    left = 30
    top = 90
    width = 480
    height = 430
    rect = pygame.Rect(left, top, width, height)
    for i in range(3):
        tmprect = pygame.Rect(left + width//3*i, top, width//3, height)
        g_BGRECT.append(tmprect)
    g_BGRECT.append(rect)

    for i in range(3):
        tmpleft = dipanLeft+i*(dipanWidth+50)
        tmp_Dipan = pygame.Rect(tmpleft, dipanTop, dipanWidth, dipanHeight)
        g_PieRect.append(tmp_Dipan)

        zhuziLeft = tmpleft +(dipanWidth - zhuziWidth)//2
        tmp_Dipan = pygame.Rect(zhuziLeft, zhuziTop, zhuziWidth, zhuziHeight)
        g_PieRect.append(tmp_Dipan)

    A_PieRect.append(g_PieRect[0])
    B_PieRect.append(g_PieRect[2])
    C_PieRect.append(g_PieRect[4])

    for i in range(g_TotalPieNums):
        tmpleft = dipanLeft + (i+1)*lap
        pieWidth = dipanWidth - lap*2*(i+1)
        tmptop = dipanTop - (i+1)*(pieHeight+2)
        tmp_Dipan = pygame.Rect(tmpleft, tmptop, pieWidth, pieHeight)
        A_PieRect.append(tmp_Dipan)
        
#绘制背景
def drawBackGround():
    # print(nameRect)
    curSurface.fill(NAVYBLUE)
    pygame.draw.rect(curSurface, YELLOW, g_BGRECT[-1],  2)

    for i in range(3):
        if g_ClickFlag[i] == 1:
            pygame.draw.rect(curSurface, RED, g_BGRECT[i],  2) #第一根柱子背景
        else:
            pygame.draw.rect(curSurface, YELLOW, g_BGRECT[i],  2) #第一根柱子背景

    # lstColor = [YELLOW, RED, WHITE, MAROON]
    for i in range(len(g_PieRect)):
        pygame.draw.rect(curSurface, GREEN, g_PieRect[i])

    for item in A_PieRect[1:]:
        pygame.draw.rect(curSurface, WHITE_D, item)
    for item in B_PieRect[1:]:
        pygame.draw.rect(curSurface, WHITE_D, item)
    for item in C_PieRect[1:]:
        pygame.draw.rect(curSurface, WHITE_D, item)
    
    curSurface.blit(headTextObj, headRectObj)
    curSurface.blit(infoTextObj3, infoRectObj3)
    curSurface.blit(infoTextObj4, infoRectObj4)
    curSurface.blit(infoHelpText, infoHelpRect)
    curSurface.blit(nameText, nameRect)
    curSurface.blit(rankTmpText, rankTmpRect)
    curSurface.blit(Level3Text, Level3Rect)
    curSurface.blit(Level4Text, Level4Rect)
    curSurface.blit(Level5Text, Level5Rect)

    curSurface.blit(textinput.get_surface(), (infoAreaLeft, nameRect.bottom+10))
    for irankinfo in lstRankInfo:
        curSurface.blit(irankinfo[0], irankinfo[1])


def calcClickFlag(pos):
    global g_TotalPieNums, g_FirstClick, g_SecondClick, g_ClickFlag, g_GAMEOVER
    if g_GAMEOVER:
        if Level3Rect.collidepoint(pos):
            g_TotalPieNums = 3
            StartGameSet()
        elif Level4Rect.collidepoint(pos):
            g_TotalPieNums = 4
            StartGameSet()
        elif Level5Rect.collidepoint(pos):
            g_TotalPieNums = 5
            StartGameSet()
        return
    # 当柱子所在的背景被点击的时候，改变相应的标记
    tmpPie = [A_PieRect, B_PieRect, C_PieRect]
    for i in range(3):
        # print(i, '---', g_ClickFlag.count(1), len(tmpPie[i]))
        if g_BGRECT[i].collidepoint(pos):
            if g_ClickFlag.count(1) == 0 and len(tmpPie[i])==1: #第一次点击时，底盘上没有饼
                break
            if g_ClickFlag[i] == 1:
                if i == g_FirstClick and g_ClickFlag.count(1)==1:#当只有1个被选中时，才能取消第1次点击的
                    g_FirstClick = -1
                    g_ClickFlag[i] = 0
                elif i == g_SecondClick:
                    g_SecondClick = -1
                    g_ClickFlag[i] = 0
            else:
                if g_ClickFlag.count(1) < 2: #如果连续点击三根柱子，则第三根不记录
                    g_ClickFlag[i] = 1
                    if g_FirstClick == -1:
                        g_FirstClick = i
                    elif g_SecondClick == -1:
                        g_SecondClick = i

    # print(g_FirstClick, g_SecondClick, g_ClickFlag)
    MovePie()
    isGameOver()
    # print("===", g_FirstClick, g_SecondClick, g_ClickFlag)
    # g_ClickFlag = [0,0,0]
    # g_FirstClick, g_SecondClick = -1, -1
g_sn_arr = []
def hannuota_genarr(arr, flagarr):
    global g_sn_arr
    [n1, n2, n3]=arr
    [a,b,c] = flagarr
    if n1==0 and n2==0:
        # print('over')
        return
    else:
        hannuota_genarr([n1-1, n2, n3], [a, c, b])
        # print([a,c])
        g_sn_arr.append([a,c])
        hannuota_genarr([n1-1, n2, n3], [b, a, c])

def autoMove():
    import time
    global g_sn_arr, g_FirstClick, g_SecondClick
    g_sn_arr = []
    hannuota_genarr([g_TotalPieNums,0,0], [0,1,2])
    # print(g_sn_arr)
    for item in g_sn_arr:
        g_FirstClick = item[0]
        g_SecondClick = item[1]
        MovePie()
        # pygame.time.wait(200)

    g_FirstClick, g_SecondClick = -1, -1

def MovePieAnimation(firstPie, left, top):
    if firstPie.left < left:
        firstPie.left += 1
    else:
        firstPie.left -= 1

    if firstPie.top < top:
        firstPie.top += 1
    else:
        firstPie.top -= 1


def MovePie():
    global g_FirstClick, g_SecondClick, g_ClickFlag, g_firstPie, g_basePie, g_animation
    
    if g_FirstClick == -1 or g_SecondClick == -1:
        return
    
    # 每一个柱子数组都是从大到小排列
    tmpPie = [A_PieRect, B_PieRect, C_PieRect]
    
    firstPie = tmpPie[g_FirstClick][-1] #移动的饼
    secondPie = tmpPie[g_SecondClick][-1] #要移动到其上的饼（含底盘）

    if firstPie.width > secondPie.width: #大盘不能放在小盘上
        g_ClickFlag = [0,0,0]
        g_FirstClick, g_SecondClick = -1, -1
        return 
    
    # print(firstPie)
    #--------------------------------------
    firstPie.left = secondPie.left + (secondPie.width-firstPie.width)//2
    firstPie.top = secondPie.top - firstPie.height-2

    tmpPie[g_FirstClick].remove(firstPie)
    tmpPie[g_SecondClick].append(firstPie)
    
    g_ClickFlag = [0,0,0]
    g_FirstClick, g_SecondClick = -1, -1
    #---------------------------------------
    g_firstPie = firstPie
    g_basePie = secondPie
    # g_animation = True


    
    
g_firstPie = ''
g_basePie = ''
g_animation = False

g_GAMEOVER = True
g_PieRect = []
A_PieRect = []
B_PieRect = []
C_PieRect = []
g_BGRECT = []
g_ClickFlag = [0,0,0]
g_FirstClick = -1
g_SecondClick = -1

def isGameOver():
    global g_GAMEOVER
    if len(C_PieRect) == g_TotalPieNums+1:
        g_GAMEOVER = True

def StartGameSet(flag_qishi=0): 
    global g_TotalSecond, g_GAMEOVER, g_FirstClick, g_SecondClick, g_ClickFlag, g_PieRect, A_PieRect, B_PieRect, C_PieRect, g_BGRECT
    g_PieRect = []
    A_PieRect = []
    B_PieRect = []
    C_PieRect = []
    g_BGRECT = []
    g_ClickFlag = [0,0,0]
    g_FirstClick = -1
    g_SecondClick = -1
    if flag_qishi == 0:
        g_GAMEOVER = True
        pygame.time.set_timer(COUNTTIMER, 0)
    else:
        g_GAMEOVER = False
        pygame.time.set_timer(COUNTTIMER, 1000)

    g_TotalSecond = 0
    genRectPos()    
    getRankInfo()
    

COUNTTIMER = pygame.USEREVENT
pygame.time.set_timer(COUNTTIMER, 0)
StartGameSet()

# genRectPos()
# getRankInfo()

while True:
    drawBackGround()
    # if g_startMoveFlag:
    #     MoveTileToBlank()
    if g_animation:
        MovePieAnimation()
  
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            calcClickFlag(event.pos)
            # numberClick(event.pos)

        elif event.type == COUNTTIMER:
            # drawBackGround(1)
            # pygame.time.set_timer(COUNTTIMER, 0) 

            infoTextObj4 = infoFontObj.render(str(g_TotalSecond)+"秒", True, YELLOW, NAVYBLUE)
            g_TotalSecond += 1
            infoRectObj4 = infoTextObj4.get_rect()
            infoRectObj4.top = infoRectObj3.bottom + 10
            infoRectObj4.left = infoAreaLeft
   
            if g_GAMEOVER and g_TotalSecond>2:
                pygame.time.set_timer(COUNTTIMER, 0) #全部选完关闭计时
                getRankInfo('write')


        elif event.type == KEYUP:
            print(event.key, chr(event.key)=='↑', pygame.key.get_mods())
           
            if event.key == 13: #重新开始
                StartGameSet(1)
            elif event.key == 32:
                autoMove()
                # pass
                
    # # textinput.update(events)
    if textinput.update(events):
        g_USERNAME = textinput.get_text()
        print(textinput.get_text())

                
    pygame.display.update()
    fpsClock.tick(FPS)