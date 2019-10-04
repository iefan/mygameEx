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
WHITE_D = (120, 120, 120)
RED_D   = (120, 0, 0)
GREEN_D = (0, 120, 0)
YELLOW = (255, 255,0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 200, 0)

blockWidth =100 
# g_ClickCount = -1
g_TotalSecond = 0

g_USERNAME = "psy"


textinput = pygame_textinput.TextInput(initial_string=g_USERNAME, font_size=24, text_color=WHITE, font_family="simhei")

curSurface = pygame.display.set_mode((630, 560), 0, 32)
pygame.display.set_caption("猜数字游戏")

# fontObj = pygame.font.Font('simsunb.ttf', 32)
numberFontObj = pygame.font.SysFont("simhei", 36)
resultFontObj = pygame.font.SysFont("simhei", 22)

fontObj = pygame.font.SysFont("simhei", 50)
headTextObj = fontObj.render("猜数字游戏", True, WHITE, NAVYBLUE)
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

rankAreaRect = pygame.Rect(infoAreaLeft, nameRect.bottom + 70, 100, 120)

lstRankInfo = []
lstRankNameAndTime = []
def getRankInfo():
    if os.path.exists(r'rankGuessNumber.dat'):
        with open(r'rankGuessNumber.dat', encoding='utf-8' ) as f:
            icount = 0
            rankTmpText = infoFontObj.render("排名", True, YELLOW, NAVYBLUE)
            rankTmpRect = rankTmpText.get_rect()
            rankTmpRect.left = infoAreaLeft
            rankTmpRect.top = nameRect.bottom + 80
            # rankTmpRect.center = (570, 400+icount*30)
            lstRankInfo.append([rankTmpText, rankTmpRect])
            # print(f.readlines())
            for irank in f.readlines():
                icount += 1
                irank = irank.strip()
                if len(irank) == 0:
                    break
                tmpname,tmpsecond = irank.split(',')
                # print(tmpsecond, type(tmpsecond))
                lstRankNameAndTime.append([int(tmpsecond[:-1]), tmpname])

                rankTmpText = infoFontObj.render(irank, True, YELLOW, NAVYBLUE)
                rankTmpRect = rankTmpText.get_rect()
                rankTmpRect.left = infoAreaLeft
                rankTmpRect.top = nameRect.bottom + 80 +icount*25
                # rankTmpRect.center = (570, 400+icount*30)
                lstRankInfo.append([rankTmpText, rankTmpRect])


m = 4
n = 4

def genRectPos():
    # global g_NumberRect
    numleft = 80
    numtop = 440
    numwidth = 50
    lap = 30

    for i in range(10):
        if i<5:
            numtop = 430
            numleft = 80 + i*(numwidth + lap)
        else:
            numtop = 490
            numleft = 80 + (i-5)*(numwidth + lap)
        numrect = pygame.Rect(numleft, numtop, numwidth, numwidth)
        g_NumberRect.append([numrect, i])
    
    OkRect = pygame.Rect(500, 460, 100,60)
    g_NumberRect.append([OkRect, -1])
        
#绘制背景
def drawBackGround():
    curSurface.fill(NAVYBLUE)
    left = 70
    top = 90
    width = 420
    height = 330
    # thinkness = 100
    rect = pygame.Rect(left, top, width, height)
    pygame.draw.rect(curSurface, YELLOW, rect,  2)

    # g_Lst_GuessResult = list(range(8))
    for i in range(len(g_Lst_GuessResult)):
        disptxt = str(g_Lst_GuessResult[i])
        if i<7:
            disptxt = "第"+str(i+1)+"次：" + disptxt
        tmpNumber = resultFontObj.render(disptxt, True, WHITE, NAVYBLUE)
        tmpNumberRect = tmpNumber.get_rect()
        tmpNumberRect.left = left+10
        tmpNumberRect.top = top + i*40 + 5
        curSurface.blit(tmpNumber, tmpNumberRect)

    # tmpguessnumber = [item[1] for item in g_UserGuessNumber]
    for i in range(10):
        numrect = g_NumberRect[i][0]
        if i not in g_UserGuessNumber:
            pygame.draw.rect(curSurface, GREEN, numrect)
            tmpNumber = numberFontObj.render(str(i), True, WHITE, GREEN)
        else:
            pygame.draw.rect(curSurface, RED, numrect)
            tmpNumber = numberFontObj.render(str(i), True, WHITE, RED)
        tmpNumberRect = tmpNumber.get_rect()
        tmpNumberRect.center = (numrect.left+ numrect.width/2, numrect.top+ numrect.width/2)
        curSurface.blit(tmpNumber, tmpNumberRect)

    
    OkRect = g_NumberRect[-1][0]
    pygame.draw.rect(curSurface, GREEN, OkRect)
    tmpNumber = numberFontObj.render('确认', True, WHITE, GREEN)
    tmpNumberRect = tmpNumber.get_rect()
    tmpNumberRect.center = (OkRect.left+ OkRect.width/2, OkRect.top+ OkRect.height/2)
    curSurface.blit(tmpNumber, tmpNumberRect)

    numberTip = infoFontObj.render(str(g_UserGuessNumber)[1:-1], True, WHITE, NAVYBLUE)
    numberTipRect = numberTip.get_rect()
    numberTipRect.left = infoAreaLeft
    numberTipRect.top = 530
    # numberTipRect.center = (570, 540)

    curSurface.blit(headTextObj, headRectObj)
    curSurface.blit(infoTextObj3, infoRectObj3)
    curSurface.blit(infoTextObj4, infoRectObj4)
    curSurface.blit(infoHelpText, infoHelpRect)
    curSurface.blit(nameText, nameRect)
    curSurface.blit(numberTip, numberTipRect)
    curSurface.blit(textinput.get_surface(), (infoAreaLeft, nameRect.bottom+10))
    pygame.draw.rect(curSurface, NAVYBLUE, rankAreaRect)
    for irankinfo in lstRankInfo:
        curSurface.blit(irankinfo[0], irankinfo[1])

g_GAMEOVER = True
g_Lst_GuessResult = []
g_NumberRect = []
g_GUESSNUMBERLIST = []
g_UserGuessNumber = []

def judgeGuessIsRight(userguessname):
    global g_GAMEOVER
    if g_GAMEOVER:
        return

    A_count = 0
    B_count = 0
    # print(g_GUESSNUMBERLIST, userguessname, '===')
    if g_GUESSNUMBERLIST == userguessname:
        g_Lst_GuessResult.append(str(userguessname) + ':) 结果正确！4A！')
        g_GAMEOVER = 1
    else:
        for i in userguessname:
            if i in g_GUESSNUMBERLIST:
                if userguessname.index(i) == g_GUESSNUMBERLIST.index(i):
                    A_count += 1
                else:
                    B_count += 1

        g_Lst_GuessResult.append('{}: {}A{}B'.format(str(userguessname), A_count, B_count))
        if len(g_Lst_GuessResult) == 7:
            g_Lst_GuessResult.append("失败，正确答案是："+ str(g_GUESSNUMBERLIST))
            g_GAMEOVER = 1


def numberClick(pos):
    global g_GAMEOVER
    if g_GAMEOVER:
        return
    # print(g_NumberRect[-1][0].collidepoint(pos), g_UserGuessNumber)
    if g_NumberRect[-1][0].collidepoint(pos) and len(g_UserGuessNumber)==4: #确认
        judgeGuessIsRight(g_UserGuessNumber.copy())
        g_UserGuessNumber.clear()
    # print(g_Lst_GuessResult)
    
    for item in g_NumberRect[:-1]:
        if item[0].collidepoint(pos):
            if item[1] in g_UserGuessNumber:
                g_UserGuessNumber.remove(item[1])
            else:
                if len(g_UserGuessNumber)<4:
                    g_UserGuessNumber.append(item[1])    
            break  
   

genRectPos()
getRankInfo()

def StartGameSet(flag_qishi=0): 
    global g_GUESSNUMBERLIST, g_Lst_GuessResult, g_NumberRect, g_GAMEOVER, g_TotalSecond
    
    g_TotalSecond = 0
    getRankInfo()
    g_GAMEOVER = False
    g_GUESSNUMBERLIST = random.sample(list(range(10)), 4)
    g_Lst_GuessResult.clear()
    
    pygame.time.set_timer(COUNTTIMER, 1000)
    # print(g_GUESSNUMBERLIST)
    


COUNTTIMER = pygame.USEREVENT
pygame.time.set_timer(COUNTTIMER, 0)
# StartGameSet()

while True:
    drawBackGround()
    # if g_startMoveFlag:
    #     MoveTileToBlank()
  
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            numberClick(event.pos)

        elif event.type == COUNTTIMER:
            # drawBackGround(1)
            # pygame.time.set_timer(COUNTTIMER, 0) 

            infoTextObj4 = infoFontObj.render(str(g_TotalSecond)+"秒", True, YELLOW, NAVYBLUE)
            g_TotalSecond += 1
            infoRectObj4 = infoTextObj4.get_rect()
            infoRectObj4.top = infoRectObj3.bottom + 10
            infoRectObj4.left = infoAreaLeft
   
            if g_GAMEOVER:
                pygame.time.set_timer(COUNTTIMER, 0) #全部选完关闭计时

                lstRankNameAndTime.append([g_TotalSecond-1, g_USERNAME])
                lstRankNameAndTime.sort()
                rankInfoStr = ""
                tmplstrankname = []
                for  isecond, iname in lstRankNameAndTime:
                    if (iname not in tmplstrankname) and len(tmplstrankname)<=3:
                        tmplstrankname.append(iname)
                        rankInfoStr += iname + "," + str(isecond) + '秒\n'

                with open(r'rankGuessNumber.dat', 'w', encoding='utf-8' ) as f:
                    f.write(rankInfoStr)
                
                # drawBackGround()
                getRankInfo()


        elif event.type == KEYUP:
            print(event.key, chr(event.key)=='↑', pygame.key.get_mods())
           
            if event.key == 13: #重新开始
                StartGameSet()
                
    # # textinput.update(events)
    if textinput.update(events):
        g_USERNAME = textinput.get_text()
        print(textinput.get_text())

                
    pygame.display.update()
    fpsClock.tick(FPS)