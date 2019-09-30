# -*- coding: utf-8 -*-
import pygame, sys, random
from pygame.locals import *
import os
import pygame_textinput

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
GREEN = (0, 200, 0)
BLUE  = (0, 0, 255)
NAVYBLUE = ( 60, 60, 100)
YELLOW = (255, 255,0)

blockWidth =100 
g_ClickCount = -1
g_TotalSecond = 0
first_ClickIcon = [0,0]
second_ClickIcon = [0,0]
g_USERNAME = "psy"
textinput = pygame_textinput.TextInput(initial_string=g_USERNAME, font_size=24, text_color=WHITE, font_family="simhei")


curSurface = pygame.display.set_mode((630, 560), 0, 32)
pygame.display.set_caption("数字华容道")

# fontObj = pygame.font.Font('simsunb.ttf', 32)
numberFontObj = pygame.font.SysFont("simhei", 36)
fontObj = pygame.font.SysFont("simhei", 50)
headTextObj = fontObj.render("数字华容道", True, WHITE, NAVYBLUE)
headRectObj = headTextObj.get_rect()
headRectObj.center = (300, 50)

infoFontObj = pygame.font.SysFont("simhei", 16)
infoTextObj = infoFontObj.render("点击次数：", True, YELLOW, NAVYBLUE)
infoRectObj = infoTextObj.get_rect()
infoRectObj.center = (580, 100)
infoTextObj2 = infoFontObj.render("0次", True, YELLOW, NAVYBLUE)
infoRectObj2 = infoTextObj2.get_rect()
infoRectObj2.center = (580, 130)

infoTextObj3 = infoFontObj.render("计  时", True, YELLOW, NAVYBLUE)
infoRectObj3 = infoTextObj3.get_rect()
infoRectObj3.center = (580, 200)

infoTextObj4 = infoFontObj.render("0秒", True, YELLOW, NAVYBLUE)
infoRectObj4 = infoTextObj4.get_rect()
infoRectObj4.center = (580, 230)

infoHelpText = infoFontObj.render("按回车重新开始", True, YELLOW, NAVYBLUE)
infoHelpRect = infoHelpText.get_rect()
infoHelpRect.center = (570, 260)

nameText = infoFontObj.render("玩家：", True, WHITE, NAVYBLUE)
nameRect = nameText.get_rect()
nameRect.center = (570, 320)

lstRankInfo = []
lstRankNameAndTime = []
flag_Start = 0

def getRankInfo():
    if os.path.exists(r'd:/myprogram/rank.dat'):
        with open(r'd:/myprogram/rank.dat', encoding='utf-8' ) as f:
            icount = 0
            rankTmpText = infoFontObj.render("排名", True, YELLOW, NAVYBLUE)
            rankTmpRect = rankTmpText.get_rect()
            rankTmpRect.center = (570, 400+icount*30)
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
                rankTmpRect.center = (570, 400+icount*30)
                lstRankInfo.append([rankTmpText, rankTmpRect])

getRankInfo()

m = 4
n = 4
lstTilesBlock = [0 for i in range(m*n)] 
#lstBlockFlag = [[0 for i in range(m)] for j in range(n)]
#lstBlockFlag_OVER = [[1 for i in range(m)] for j in range(n)]
def generatePos():
    for i in range(m*n):
        row = i // m
        col = i % m
        lstTilesBlock[i] = [pygame.Rect(70+col*(blockWidth+5),110+row*(blockWidth+5), blockWidth, blockWidth), i+1, '0000']

generatePos() #生成所有棋子的位置数据

#绘制背景
def drawBackGround():
    curSurface.fill(NAVYBLUE)
    for i in range(m*n-1):
        curblock = lstTilesBlock[i]
        pygame.draw.rect(curSurface, GREEN, curblock[0])
        tmpNumber = numberFontObj.render(str(curblock[1]), True, WHITE, GREEN)
        tmpNumberRect = tmpNumber.get_rect()
        tmpNumberRect.center = (curblock[0].left+ blockWidth/2, curblock[0].top+ blockWidth/2)
        curSurface.blit(tmpNumber, tmpNumberRect)

    pygame.draw.rect(curSurface, YELLOW, [65, 105, 425, 425],7)
    curSurface.blit(headTextObj, headRectObj)
    curSurface.blit(infoTextObj, infoRectObj)
    curSurface.blit(infoTextObj2, infoRectObj2)
    curSurface.blit(infoTextObj3, infoRectObj3)
    curSurface.blit(infoTextObj4, infoRectObj4)
    curSurface.blit(infoHelpText, infoHelpRect)
    curSurface.blit(nameText, nameRect)
    curSurface.blit(textinput.get_surface(), (540, 340))
    for irankinfo in lstRankInfo:
        curSurface.blit(irankinfo[0], irankinfo[1])


def printTile(pos):
    for i in range(m*n):
        if lstTilesBlock[i][0].collidepoint(pos):
            print(lstTilesBlock[i][1], lstTilesBlock[i][2])

def findCanMoveTiles():
    for i in range(m*n):
        lstTilesBlock[i][2] = '0000' #左上右下标志
        if lstTilesBlock[i][1] == 16: #找到空格
            row = i//m
            col = i % n
            top     = (row-1)>=0  and (row-1)*m+col      or -1
            bottom  = (row+1)<m and (row+1)*m+col      or -1
            left    = (col-1)>=0  and row*m + (col-1)    or -1
            right   = (col+1)<n and row*m + (col+1)    or -1

            # print([left, top, right, bottom])
            icount = -1
            for item in [right, bottom, left, top]:
                icount += 1
                if item!=-1:
                    tmp = list(lstTilesBlock[item][2])
                    tmp[icount] = '1'
                    lstTilesBlock[item][2] = ''.join(tmp)
                    print(lstTilesBlock[item][1], lstTilesBlock[item][2])

findCanMoveTiles()

DISPFIRST = pygame.USEREVENT #创建自定义事件，第一次全部显示供用户记忆
pygame.time.set_timer(DISPFIRST, 5000)

DISPINFOTEXT = pygame.USEREVENT+1 #创建自定义事件，计时
pygame.time.set_timer(DISPINFOTEXT, 0)

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

    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            printTile(event.pos)
            # print(mouse_x, mouse_y)
        elif event.type == DISPFIRST:
            if flag_Start == 1:
                lstBlockFlag = [[0 for i in range(m)] for j in range(n)]
                g_ClickCount = 0
                pygame.time.set_timer(DISPFIRST, 0)
                pygame.time.set_timer(DISPINFOTEXT, 1000)

        elif event.type == DISPINFOTEXT:
            infoTextObj4 = infoFontObj.render(str(g_TotalSecond)+"秒", True, YELLOW, NAVYBLUE)
            g_TotalSecond += 1
            infoRectObj4 = infoTextObj4.get_rect()
            infoRectObj4.center = (580, 230)

            #程序结束
            if lstBlockFlag == lstBlockFlag_OVER and g_ClickCount > 1:
                # print(lstBlockFlag)
                pygame.time.set_timer(DISPINFOTEXT, 0) #全部选完关闭计时

                lstRankNameAndTime.append([g_TotalSecond-1, g_USERNAME])
                lstRankNameAndTime.sort()
                rankInfoStr = ""
                for  isecond, iname in lstRankNameAndTime[:3]:
                    rankInfoStr += iname + "," + str(isecond) + '秒\n'

                with open(r'd:/myprogram/rank.dat', 'w') as f:
                    f.write(rankInfoStr)

                lstRankNameAndTime = []
                getRankInfo() #调用最新排名
                    
            # print(g_TotalSecond)

        elif event.type == KEYUP:
            print(event.key, chr(event.key)=='↑', pygame.key.get_mods())
            if event.key == 13: #重新开始
                # if textinput.update(events): #获取用户名称
                #     g_USERNAME = textinput.get_text()
                #     print(g_USERNAME)
                flag_Start = 1
                g_ClickCount = -1
                g_TotalSecond = 0
                first_ClickIcon = [0,0]
                second_ClickIcon = [0,0]
                lstBlockFlag = [[1 for i in range(m)] for j in range(n)]
                random.shuffle(lstIcon) #将图标排列随机化
#                lstRankNameAndTime = []
#                getRankInfo() #调用最新排名
  
                infoTextObj2 = infoFontObj.render("0次", True, YELLOW, NAVYBLUE)
                infoRectObj2 = infoTextObj2.get_rect()
                infoRectObj2.center = (580, 130)
                pygame.time.set_timer(DISPFIRST, 5000) #玩家记忆时间
                # pygame.time.set_timer(DISPINFOTEXT, 1000) #重启计时器
   
    # textinput.update(events)
    if textinput.update(events):
        g_USERNAME = textinput.get_text()
        print(textinput.get_text())

    if flag_Start == 1:
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
