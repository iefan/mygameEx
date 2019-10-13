# -*- coding: utf-8 -*-
import pygame, sys, random, math
from pygame.locals import *
import os
import pygame_textinput

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

g_TotalSecond = 0
g_USERNAME = "psy"

textinput = pygame_textinput.TextInput(initial_string=g_USERNAME, font_size=24, text_color=WHITE, font_family="simhei")

curSurface = pygame.display.set_mode((630, 560), 0, 32)
pygame.display.set_caption("模仿记忆游戏")

# fontObj = pygame.font.Font('simsunb.ttf', 32)
fontObj = pygame.font.SysFont("simhei", 50)
headTextObj = fontObj.render("模仿记忆游戏", True, WHITE, NAVYBLUE)
headRectObj = headTextObj.get_rect()
headRectObj.center = (300, 50)

infoFontObj = pygame.font.SysFont("simhei", 18)
infoAreaTop = 100
infoAreaLeft = 510
infoTextObj1 = infoFontObj.render("成功次数", True, YELLOW, NAVYBLUE)
infoRectObj1 = infoTextObj1.get_rect()
infoRectObj1.top = infoAreaTop + 10
infoRectObj1.left = infoAreaLeft

infoTextObj2 = infoFontObj.render("0次", True, YELLOW, NAVYBLUE)
infoRectObj2 = infoTextObj2.get_rect()
infoRectObj2.top = infoRectObj1.bottom + 10
infoRectObj2.left = infoAreaLeft

# infoTextObj3 = infoFontObj.render("计  时", True, YELLOW, NAVYBLUE)
# infoRectObj3 = infoTextObj3.get_rect()
# infoRectObj3.top = infoRectObj2.bottom + 30
# infoRectObj3.left = infoAreaLeft

# infoTextObj4 = infoFontObj.render("0秒", True, YELLOW, NAVYBLUE)
# infoRectObj4 = infoTextObj4.get_rect()
# infoRectObj4.top = infoRectObj3.bottom + 10
# infoRectObj4.left = infoAreaLeft
# # infoRectObj4.center = (580, 230)

infoHelpText = infoFontObj.render("按回车开始", True, YELLOW, NAVYBLUE)
infoHelpRect = infoHelpText.get_rect()
infoHelpRect.top = infoRectObj2.bottom + 30
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

successText = infoFontObj.render("提示", True, YELLOW, NAVYBLUE)
successRect = successText.get_rect()
successRect.left = infoAreaLeft
successRect.top = 480

BEEP1 = pygame.mixer.Sound('sound/beep1.ogg')
BEEP2 = pygame.mixer.Sound('sound/beep2.ogg')
BEEP3 = pygame.mixer.Sound('sound/beep3.ogg')
BEEP4 = pygame.mixer.Sound('sound/beep4.ogg')

lstRankInfo = []
lstRankNameAndTime = []
def getRankInfo(flag = "read"):
    global lstRankInfo, lstRankNameAndTime
    if flag == 'read':
        lstRankNameAndTime = []
        if os.path.exists(r'rankSim.dat'):
            with open(r'rankSim.dat', encoding='utf-8' ) as f:
                icount = 0
                
                for irank in f.readlines():
                    
                    irank = irank.strip()
                    if len(irank) == 0:
                        break
                    tmpsecond, tmpname = irank.split(',')
                    # print(tmplevel, type(g_TotalPieNums))
                    lstRankNameAndTime.append([int(tmpsecond), tmpname])
                
                lstRankInfo = []
                lstRankNameAndTime.sort(reverse=True)
                firstThreeName = []
                for item in lstRankNameAndTime:
                    if item[1] not in firstThreeName and len(firstThreeName)<3:
                        firstThreeName.append(item[1])
                    else:
                        continue

                    icount += 1
                    rankTmpText = infoFontObj.render(item[1]+":"+str(item[0])+"次", True, YELLOW, NAVYBLUE)
                    rankTmpRect = rankTmpText.get_rect()
                    rankTmpRect.left = infoAreaLeft
                    rankTmpRect.top = nameRect.bottom + 80 +icount*25
                    lstRankInfo.append([rankTmpText, rankTmpRect])
                    # print(lstRankNameAndTime)
              
    elif flag=="write":
        if g_COUNT_SUCCESS>0:
            lstRankNameAndTime.append([g_COUNT_SUCCESS, g_USERNAME])
            lstRankNameAndTime.sort(reverse=True)
            rankInfoStr = ""
            for item in lstRankNameAndTime:
                rankInfoStr += str(item[0]) + "," + item[1] + '\n'
            with open(r'rankSim.dat', 'w', encoding='utf-8' ) as f:
                f.write(rankInfoStr)

            getRankInfo()



g_lstBlockRect = []
g_BEEP_FLAG = []
def generatePos(flagRight = 0):
    g_lstBlockRect.clear()

    blocktop = 100
    blockleft = 60
    blockwidth = 200 

    for i in range(2):
        for j in range(2):
            g_lstBlockRect.append(pygame.Rect(blockleft+j*blockwidth, blocktop+i*blockwidth, blockwidth, blockwidth))

g_Beep_Index = 0
#绘制背景
def drawBackGround(slash = 0):
    global g_slashcount, g_lstslash, BEEP1, BEEP2, BEEP3, BEEP4, g_BEEP_FLAG, g_Beep_Index
    curSurface.fill(NAVYBLUE)
    
    # lstBeep = [BEEP1, BEEP2, BEEP3, BEEP4]
    lstColor = [YELLOW_D, RED_D, GREEN_D, WHITE_D]
    lstColor2 = [YELLOW, RED, GREEN, WHITE]
    for i in range(4):
        if slash == 0:
            pygame.draw.rect(curSurface, lstColor[i], g_lstBlockRect[i])
        elif slash == 1 or slash == 2:

            if g_lstslash[i]==1:
                # print(g_Beep_Index, g_BEEP_FLAG, i, g_lstslash, gg_lstslashAll.index(g_lstslash))
                # # ibeepindex = gg_lstslashAll.index(g_lstslash)
                # if g_Beep_Index < len(g_BEEP_FLAG):
                #     if slash == 1 and g_BEEP_FLAG[g_Beep_Index] != -1 :
                #         lstBeep[g_BEEP_FLAG[g_Beep_Index]].play()
                #         g_BEEP_FLAG[g_Beep_Index] = -1
                #         g_Beep_Index += 1
                pygame.draw.rect(curSurface, lstColor2[i], g_lstBlockRect[i])
            else:
                pygame.draw.rect(curSurface, lstColor[i], g_lstBlockRect[i])
  
    curSurface.blit(headTextObj, headRectObj)
    curSurface.blit(infoTextObj1, infoRectObj1)
    curSurface.blit(infoTextObj2, infoRectObj2)
    # curSurface.blit(infoTextObj3, infoRectObj3)
    # curSurface.blit(infoTextObj4, infoRectObj4)
    curSurface.blit(infoHelpText, infoHelpRect)
    curSurface.blit(nameText, nameRect)
    curSurface.blit(successText, successRect)
    curSurface.blit(rankTmpText, rankTmpRect)
    curSurface.blit(textinput.get_surface(), (540, nameRect.bottom+10))

    for irankinfo in lstRankInfo:
        curSurface.blit(irankinfo[0], irankinfo[1])

def genRandlist(n=5):
    global g_CurSn
    lstbeepFlag = []
    g_CurSn = ''
    # n = 5
    lstrandslash = []
    for i in range(n):
        tmp = [0,0,0,0]
        tmpint = random.randint(0,3)
        lstbeepFlag.append(tmpint)

        tmp[tmpint] = 1
        g_CurSn += str(pow(2, tmpint)) #将每一次显示转换为对应的十进制
        lstrandslash.append(tmp.copy())
        lstrandslash.append([0,0,0,0])
        # print(lstrandslash)
    lstrandslash.append([0,0,0,0])
    return [lstrandslash.copy(), lstbeepFlag.copy()]

# genRandlist()
def StartGameSet(flag_qishi=0):
    global successText, g_BEEP_FLAG, g_GAMESTART, COUNTTIMER, g_Slash, g_slashcount,g_lstslash, g_CurSn,g_CurSn_user,gg_lstslashAll, g_COUNT_SUCCESS
    generatePos()
    g_GAMESTART = flag_qishi
    getRankInfo()
    g_Slash = 0
    g_slashcount = 0
    g_lstslash = [0,0,0,0]
    g_CurSn = ''
    g_CurSn_user = ''
    gg_lstslashAll = []
    g_BEEP_FLAG = []
    g_COUNT_SUCCESS = 0
    successText = infoFontObj.render("提示", True, YELLOW, NAVYBLUE)
    
g_GAMESTART = 0

COUNTTIMER = pygame.USEREVENT
pygame.time.set_timer(COUNTTIMER, 0)
TIMERUSERDISP = pygame.USEREVENT+1 #用来显示玩家点击时亮度设置
pygame.time.set_timer(TIMERUSERDISP, 0)
GAMETIMER = pygame.USEREVENT+2
pygame.time.set_timer(GAMETIMER, 0)

StartGameSet()
g_Slash = 0
g_slashcount = 0
g_lstslash = [0,0,0,0]
g_CurSn = ''
g_CurSn_user = ''
gg_lstslashAll = []
g_COUNT_SUCCESS = 0
g_GAME_CONTROL_LIST = list(range(1,21))*2
g_GAME_CONTROL_LIST.sort()
while True:
    drawBackGround(g_Slash)
  
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == GAMETIMER:
            g_lstslash = [0,0,0,0]
            if g_GAMESTART == 1:
                g_GAMESTART = 0
                g_COUNT_SUCCESS = 0
                pygame.time.set_timer(COUNTTIMER, 0)
                pygame.time.set_timer(TIMERUSERDISP, 0)
                pygame.time.set_timer(GAMETIMER, 0)
                print("false", )
                successText = infoFontObj.render("超时挑战失败！", True, RED, NAVYBLUE)
                getRankInfo('write')

                # g_Slash = 1
                # g_slashcount = 0
                # pygame.time.set_timer(COUNTTIMER, 300) #开启新一轮
            pygame.time.set_timer(GAMETIMER, 0) #结束当前

        elif event.type == TIMERUSERDISP:
            g_lstslash = [0,0,0,0]
            g_Slash == 2
            if len(g_CurSn) == len(g_CurSn_user):
                if g_CurSn == g_CurSn_user:
                    g_COUNT_SUCCESS += 1
                    infoTextObj2 = infoFontObj.render(str(g_COUNT_SUCCESS)+"次", True, YELLOW, NAVYBLUE)
                    
                    successText = infoFontObj.render("恭喜，成功！", True, YELLOW, NAVYBLUE)
                    pygame.time.set_timer(COUNTTIMER, 300)
                    pygame.time.set_timer(GAMETIMER, 0)

                    print("true!")
                else:
                    g_GAMESTART = 0
                    g_COUNT_SUCCESS = 0
                    pygame.time.set_timer(COUNTTIMER, 0)
                    pygame.time.set_timer(TIMERUSERDISP, 0)
                    pygame.time.set_timer(GAMETIMER, 0)
                    print("false", )
                    successText = infoFontObj.render("遗憾，失败！", True, RED, NAVYBLUE)
                    getRankInfo('write')
                    

                g_Slash = 1
                g_CurSn_user = ''
            pygame.time.set_timer(TIMERUSERDISP, 0)

        elif event.type == MOUSEBUTTONUP:
    #         # mouse_x, mouse_y = event.pos
            if g_GAMESTART == 1 and g_Slash == 2: #当显示结束才可以点击
                g_lstslash = [0,0,0,0]
                for i in range(4):                
                    if g_lstBlockRect[i].collidepoint(event.pos):
                        g_CurSn_user += str(pow(2,i))
                        g_lstslash[i] = 1
                        pygame.time.set_timer(TIMERUSERDISP, 300)
                        g_Slash == 1
                print(g_CurSn, g_CurSn_user, g_CurSn==g_CurSn_user, g_lstslash)
                
        
        elif event.type == COUNTTIMER:
            # drawBackGround(1)
            # g_Slash = 0
            if g_slashcount == 0 and g_Slash == 1:
                [gg_lstslashAll, g_BEEP_FLAG ]= genRandlist(g_GAME_CONTROL_LIST[g_COUNT_SUCCESS]) #新一轮游戏
                g_Slash = 1
                g_lstslash = [0,0,0,0]
                g_Beep_Index = 0
                # g_BEEP_FLAG = [0]*len(gg_lstslashAll)

            if g_slashcount<len(gg_lstslashAll) and g_Slash==1:
                g_lstslash = gg_lstslashAll[g_slashcount]
                # print(g_slashcount, g_lstslash)
                g_slashcount += 1
                
            else:
                g_Slash = 2 #开始玩家点击
                g_slashcount = 0
                g_lstslash = [0,0,0,0]
                pygame.time.set_timer(COUNTTIMER, 0)
                # print(gg_lstslashAll, len(gg_lstslashAll))
                pygame.time.set_timer(GAMETIMER, len(gg_lstslashAll)*800) #启动游戏

            # # print(g_slashcount, '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
           

        elif event.type == KEYUP:
            print(event.key, chr(event.key)=='↑', pygame.key.get_mods())
            if event.key == 13: #回车开始
                StartGameSet(1)
                g_COUNT_SUCCESS = 0
                infoTextObj2 = infoFontObj.render(str(g_COUNT_SUCCESS)+"次", True, YELLOW, NAVYBLUE)

                g_Slash = 1
                pygame.time.set_timer(COUNTTIMER, 300) #启动游戏
   
      
    # # textinput.update(events)
    if textinput.update(events):
        g_USERNAME = textinput.get_text()
        print(textinput.get_text())

                
    pygame.display.update()
    fpsClock.tick(FPS)
