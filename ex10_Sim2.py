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
infoAreaLeft = 530
infoTextObj1 = infoFontObj.render("成功次数", True, YELLOW, NAVYBLUE)
infoRectObj1 = infoTextObj1.get_rect()
infoRectObj1.top = infoAreaTop + 10
infoRectObj1.left = infoAreaLeft

infoTextObj2 = infoFontObj.render("0次", True, YELLOW, NAVYBLUE)
infoRectObj2 = infoTextObj2.get_rect()
infoRectObj2.top = infoRectObj1.bottom + 10
infoRectObj2.left = infoAreaLeft

infoTextObj3 = infoFontObj.render("计  时", True, YELLOW, NAVYBLUE)
infoRectObj3 = infoTextObj3.get_rect()
infoRectObj3.top = infoRectObj2.bottom + 30
infoRectObj3.left = infoAreaLeft

infoTextObj4 = infoFontObj.render("0秒", True, YELLOW, NAVYBLUE)
infoRectObj4 = infoTextObj4.get_rect()
infoRectObj4.top = infoRectObj3.bottom + 10
infoRectObj4.left = infoAreaLeft
# infoRectObj4.center = (580, 230)

infoHelpText = infoFontObj.render("按回车开始", True, YELLOW, NAVYBLUE)
infoHelpRect = infoHelpText.get_rect()
infoHelpRect.top = infoRectObj4.bottom + 30
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

BEEP1 = pygame.mixer.Sound('sound/beep1.ogg')

def getRankInfo():
    if os.path.exists(r'rankSim.dat'):
        with open(r'rankSim.dat', encoding='utf-8' ) as f:
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



g_lstBlockRect = []
def generatePos(flagRight = 0):
    g_lstBlockRect.clear()

    blocktop = 100
    blockleft = 80
    blockwidth = 200 

    for i in range(2):
        for j in range(2):
            g_lstBlockRect.append(pygame.Rect(blockleft+j*blockwidth, blocktop+i*blockwidth, blockwidth, blockwidth))

g_slashcount = 0
#绘制背景
def drawBackGround(slash = 0):
    global g_slashcount
    curSurface.fill(NAVYBLUE)
    
    lstColor = [YELLOW_D, RED_D, GREEN_D, WHITE_D]
    lstColor2 = [YELLOW, RED, GREEN, WHITE]
    for i in range(4):
        if slash == 0:
            pygame.draw.rect(curSurface, lstColor[i], g_lstBlockRect[i])
        elif slash == 1:
            print('-----', i, g_slashcount)
            if i==g_slashcount:
                pygame.draw.rect(curSurface, lstColor2[i], g_lstBlockRect[i])
            else:
                pygame.draw.rect(curSurface, lstColor[i], g_lstBlockRect[i])
  
    curSurface.blit(headTextObj, headRectObj)
    curSurface.blit(infoTextObj1, infoRectObj1)
    curSurface.blit(infoTextObj2, infoRectObj2)
    curSurface.blit(infoTextObj3, infoRectObj3)
    curSurface.blit(infoTextObj4, infoRectObj4)
    curSurface.blit(infoHelpText, infoHelpRect)
    curSurface.blit(nameText, nameRect)
    curSurface.blit(textinput.get_surface(), (540, 340))


def StartGameSet(flag_qishi=0):
    global g_GAMESTART, COUNTTIMER
    generatePos()
    g_GAMESTART = 0
    
g_GAMESTART = 0

COUNTTIMER = pygame.USEREVENT
pygame.time.set_timer(COUNTTIMER, 0)

StartGameSet()
g_Slash = 0
while True:
    drawBackGround(g_Slash)
    # if g_startMoveFlag:
    #     MoveTileToBlank()
  
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    #     elif event.type == MOUSEBUTTONUP:
    #         # mouse_x, mouse_y = event.pos
    #         # printTile(event.pos)
    #         if g_GAMESTART == 1:
    #             flag_exit_move = 0
    #             for item in lstTilesBlock:                
    #                 if item[0].collidepoint(event.pos) and (item in g_canMoveTiles) and g_mouseLock==1:
    #                     if item[2] == '1000':
    #                         flag_exit_move = 1
    #                         orientation = K_LEFT
    #                     elif item[2] == '0100':
    #                         flag_exit_move = 1
    #                         orientation = K_UP
    #                     elif item[2] == '0010':
    #                         flag_exit_move = 1
    #                         orientation = K_RIGHT
    #                     elif item[2] == '0001':
    #                         flag_exit_move = 1
    #                         orientation = K_DOWN
                        
    #                     setMoveState(item, flag_exit_move, orientation)
    #                     if flag_exit_move == 1:
    #                         infoTextObj2 = infoFontObj.render(str(g_ClickCount)+"步", True, YELLOW, NAVYBLUE)
    #                         infoRectObj2 = infoTextObj2.get_rect()
    #                         infoRectObj2.center = (580, 150)
    #                     # print(infoRectObj2)
                    
    #         # print(mouse_x, mouse_y)
        
        elif event.type == COUNTTIMER:
            # drawBackGround(1)
            g_Slash = 0
            g_slashcount += 1
            print(g_slashcount, '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            if g_slashcount == 4:
                g_slashcount = 0
    #        pygame.time.set_timer(COUNTTIMER, 0) 

    #         infoTextObj4 = infoFontObj.render(str(g_TotalSecond)+"秒", True, YELLOW, NAVYBLUE)
    #         g_TotalSecond += 1
    #         infoRectObj4 = infoTextObj4.get_rect()
    #         infoRectObj4.center = (580, 230)

    #         # infoTextObj2 = infoFontObj.render(str(g_ClickCount)+"次", True, YELLOW, NAVYBLUE)
    #         # g_TotalSecond += 1
    #         # infoRectObj2 = infoTextObj4.get_rect()
    #         # infoRectObj2.center = (580, 130)

    #         #程序结束
    #         overStr = ""
    #         overFinaly = ''.join('%s' % id for id in range(1,17))
    #         for item in lstTilesBlock:
    #             overStr += str(item[1])
    #         # print(overStr)
    #         # print(overFinaly)
    #         if overStr == overFinaly:
    #             g_GAMESTART = 0
    #             # print(lstBlockFlag)
    #             pygame.time.set_timer(COUNTTIMER, 0) #全部选完关闭计时

    #             lstRankNameAndTime.append([g_TotalSecond-1, g_USERNAME])
    #             lstRankNameAndTime.sort()
    #             rankInfoStr = ""
    #             tmplstrankname = []
    #             for  isecond, iname in lstRankNameAndTime:
    #                 if (iname not in tmplstrankname) and len(tmplstrankname)<=3:
    #                     tmplstrankname.append(iname)
    #                     rankInfoStr += iname + "," + str(isecond) + '秒\n'

    #             with open(r'rankSim.dat', 'w', encoding='utf-8' ) as f:
    #                 f.write(rankInfoStr)

    #             lstRankNameAndTime = []
    #             getRankInfo() #调用最新排名
                    
    #         # print(g_TotalSecond)

        elif event.type == KEYUP:
            print(event.key, chr(event.key)=='↑', pygame.key.get_mods())
            if event.key == 13: #重新开始
                g_Slash = 1
                
    #             StartGameSet(1)
    #             g_GAMESTART = 1
                pygame.time.set_timer(COUNTTIMER, 3000) #启动游戏
                
    #             # infoTextObj2 = infoFontObj.render("0次", True, YELLOW, NAVYBLUE)
    #             # infoRectObj2 = infoTextObj2.get_rect()
    #             # infoRectObj2.center = (580, 130)
      
    # # textinput.update(events)
    if textinput.update(events):
        g_USERNAME = textinput.get_text()
        print(textinput.get_text())

                
    pygame.display.update()
    fpsClock.tick(FPS)
