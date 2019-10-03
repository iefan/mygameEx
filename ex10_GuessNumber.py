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
g_ClickCount = -1
g_TotalSecond = 0

g_USERNAME = "psy"

textinput = pygame_textinput.TextInput(initial_string=g_USERNAME, font_size=24, text_color=WHITE, font_family="simhei")

curSurface = pygame.display.set_mode((630, 560), 0, 32)
pygame.display.set_caption("猜数字游戏")

# fontObj = pygame.font.Font('simsunb.ttf', 32)
numberFontObj = pygame.font.SysFont("simhei", 36)
resultFontObj = pygame.font.SysFont("simhei", 26)

fontObj = pygame.font.SysFont("simhei", 50)
headTextObj = fontObj.render("猜数字游戏", True, WHITE, NAVYBLUE)
headRectObj = headTextObj.get_rect()
headRectObj.center = (300, 50)

infoFontObj = pygame.font.SysFont("simhei", 16)
infoTextObj = infoFontObj.render("成绩", True, YELLOW, NAVYBLUE)
infoRectObj = infoTextObj.get_rect()
infoRectObj.center = (580, 120)
infoTextObj2 = infoFontObj.render("0步", True, YELLOW, NAVYBLUE)
infoRectObj2 = infoTextObj2.get_rect()
infoRectObj2.center = (580, 150)

infoTextObj3 = infoFontObj.render("计  时", True, YELLOW, NAVYBLUE)
infoRectObj3 = infoTextObj3.get_rect()
infoRectObj3.center = (580, 200)

infoTextObj4 = infoFontObj.render("0秒", True, YELLOW, NAVYBLUE)
infoRectObj4 = infoTextObj4.get_rect()
infoRectObj4.center = (580, 230)

infoHelpText = infoFontObj.render("按回车开始", True, YELLOW, NAVYBLUE)
infoHelpRect = infoHelpText.get_rect()
infoHelpRect.center = (575, 270)

nameText = infoFontObj.render("玩家：", True, WHITE, NAVYBLUE)
nameRect = nameText.get_rect()
nameRect.center = (570, 320)


def getRankInfo():
    if os.path.exists(r'rankSlide.dat'):
        with open(r'rankSlide.dat', encoding='utf-8' ) as f:
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


m = 4
n = 4


#绘制背景
def drawBackGround():
    curSurface.fill(NAVYBLUE)
    left = 80
    top = 90
    width = 400
    height = 330
    # thinkness = 100
    rect = pygame.Rect(left, top, width, height)
    pygame.draw.rect(curSurface, YELLOW, rect,  2)

    numleft = 80
    numtop = 440
    numwidth = 50
    lap = 30

    lst_GuessResult = list(range(8))
    for i in range(len(lst_GuessResult)):
        tmpNumber = resultFontObj.render("第"+str(i+1)+"次：", True, WHITE, NAVYBLUE)
        tmpNumberRect = tmpNumber.get_rect()
        tmpNumberRect.left = left+10
        tmpNumberRect.top = top + i*40 + 5
        curSurface.blit(tmpNumber, tmpNumberRect)

    for i in range(10):
        if i<5:
            numtop = 430
            numleft = 80 + i*(numwidth + lap)
        else:
            numtop = 490
            numleft = 80 + (i-5)*(numwidth + lap)
        numrect = pygame.Rect(numleft, numtop, numwidth, numwidth)
        pygame.draw.rect(curSurface, GREEN, numrect)
        tmpNumber = numberFontObj.render(str(i), True, WHITE, GREEN)
        tmpNumberRect = tmpNumber.get_rect()
        tmpNumberRect.center = (numrect.left+ numwidth/2, numrect.top+ numwidth/2)
        curSurface.blit(tmpNumber, tmpNumberRect)
    
    OkRect = pygame.Rect(500, 460, 100,60)
    pygame.draw.rect(curSurface, GREEN, OkRect)
    tmpNumber = numberFontObj.render('确认', True, WHITE, GREEN)
    tmpNumberRect = tmpNumber.get_rect()
    tmpNumberRect.center = (OkRect.left+ OkRect.width/2, OkRect.top+ OkRect.height/2)
    curSurface.blit(tmpNumber, tmpNumberRect)


    # center = (left+width/2, top+width/2)
    # pygame.draw.arc(curSurface, YELLOW, (left, top, width, width), 0, math.pi/4*8, thinkness)
    # tmpx = int(center[0]-width*math.cos(math.pi/4)/2)
    # tmpy = int(center[0]-width*math.sin(math.pi/4)/2)
    # pygame.draw.aaline(curSurface, BLACK, center, (tmpx, tmpy))
    # pygame.draw.aaline(curSurface, BLACK, (left, top), (left+width, top))
    # pygame.draw.aaline(curSurface, BLACK, (left, top), (left, top+width))
    # pygame.draw.aaline(curSurface, BLACK, (left+width, top), (left+width, top+width))
    # pygame.draw.aaline(curSurface, BLACK, (left, top+width), (left+width, top+width))
    # for i in range(int(math.pi/4*100+2), int(math.pi/4*3*100)):
        # print(i)
        # pygame.draw.arc(curSurface, YELLOW, (top, left, width, width), math.pi/4, i/100, 80)
    # if slash == 0:
    #     pygame.draw.arc(curSurface, YELLOW_D, (left, top, width, width), math.pi/4, math.pi/4*3, thinkness)
    #     pygame.draw.arc(curSurface, RED_D, (left, top, width, width), math.pi/4*3, math.pi/4*5, thinkness)
    #     pygame.draw.arc(curSurface, GREEN_D, (left, top, width, width), math.pi/4*5, math.pi/4*7, thinkness)
    #     pygame.draw.arc(curSurface, WHITE_D, (left, top, width, width), math.pi/4*7, math.pi/4, thinkness)
    # elif slash == 1:
    #     pygame.draw.arc(curSurface, YELLOW, (left, top, width, width), math.pi/4, math.pi/4*3, thinkness)
    #     pygame.draw.arc(curSurface, RED, (left, top, width, width), math.pi/4*3, math.pi/4*5, thinkness)
    #     pygame.draw.arc(curSurface, GREEN, (left, top, width, width), math.pi/4*5, math.pi/4*7, thinkness)
    #     pygame.draw.arc(curSurface, WHITE, (left, top, width, width), math.pi/4*7, math.pi/4, thinkness)
        # pygame.time.wait(2000)
    # for i in range(m*n):
    #     curblock = lstTilesBlock[i]
    #     if curblock[1] != 16:
    #         pygame.draw.rect(curSurface, GREEN, curblock[0])
    #         tmpNumber = numberFontObj.render(str(curblock[1]), True, WHITE, GREEN)
    #         tmpNumberRect = tmpNumber.get_rect()
    #         tmpNumberRect.center = (curblock[0].left+ blockWidth/2, curblock[0].top+ blockWidth/2)
    #         curSurface.blit(tmpNumber, tmpNumberRect)

    # pygame.draw.rect(curSurface, YELLOW, [65, 105, 425, 425],7)
    # center_posx = 270
    # center_posy = 300
    # radius = 180
    # left = center_posx - radius
    # top = center_posy - radius
    # pygame.gfxdraw.aacircle(curSurface, center_posx, center_posy, radius, BLACK)
    # pygame.gfxdraw.filled_circle(curSurface, center_posx, center_posy, radius, BLACK)
    # pygame.gfxdraw.pie(curSurface, 100, 100, 100, 0, 30, YELLOW)
    # for i in range(0, 30):
    #     pygame.gfxdraw.pie(curSurface, 100, 100, 100, 0, i, YELLOW)
    # pygame.draw.arc(curSurface, YELLOW, (left, top, left+radius, top+radius), math.pi/4*3, math.pi/4, 80)
  
    curSurface.blit(headTextObj, headRectObj)
    curSurface.blit(infoTextObj, infoRectObj)
    curSurface.blit(infoTextObj2, infoRectObj2)
    curSurface.blit(infoTextObj3, infoRectObj3)
    curSurface.blit(infoTextObj4, infoRectObj4)
    curSurface.blit(infoHelpText, infoHelpRect)
    curSurface.blit(nameText, nameRect)
    curSurface.blit(textinput.get_surface(), (540, 340))
    # for irankinfo in lstRankInfo:
    #     curSurface.blit(irankinfo[0], irankinfo[1])

g_GUESSNUMBERLIST = []
g_UserGuessNumber = []
def StartGameSet(flag_qishi=0): 
    global g_GUESSNUMBERLIST = random.sample(list(range(10)), 4)
#     global g_GAMESTART,g_TotalSecond,g_ClickCount, g_canMoveTiles, lstTilesBlock, g_startMoveFlag, g_keyLock, g_mouseLock, lstRankInfo, lstRankNameAndTime
#     lstRankInfo = []
#     lstRankNameAndTime = []
#     g_startMoveFlag = 0
#     g_keyLock = 1
#     g_mouseLock = 1
#     g_TotalSecond = 0
#     g_ClickCount = 1

#     getRankInfo()
#     lstTilesBlock = [0 for i in range(m*n)] 
#     generatePos(flag_qishi) #生成所有棋子的位置数据
#     pygame.time.set_timer(COUNTTIMER, 0)
#     g_GAMESTART = 0
#     g_canMoveTiles = findCanMoveTiles()
    

StartGameSet()
COUNTTIMER = pygame.USEREVENT
pygame.time.set_timer(COUNTTIMER, 0)

while True:
    drawBackGround()
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
            pygame.time.set_timer(COUNTTIMER, 0) 

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

    #             with open(r'rankSlide.dat', 'w', encoding='utf-8' ) as f:
    #                 f.write(rankInfoStr)

    #             lstRankNameAndTime = []
    #             getRankInfo() #调用最新排名
                    
    #         # print(g_TotalSecond)

        elif event.type == KEYUP:
            print(event.key, chr(event.key)=='↑', pygame.key.get_mods())
    #         # g_canMoveTiles = findCanMoveTiles()
    #         # print('g_keyLock', g_keyLock)
    #         if g_GAMESTART == 1:
    #             item = ''
    #             flag_exit_move = 0
    #             if event.key == K_DOWN and g_keyLock == 1:
    #                 for item in g_canMoveTiles:
    #                     if item[2][3] == '1':
    #                         flag_exit_move = 1
    #                         break 
    #             elif event.key == K_UP and g_keyLock == 1:
    #                 for item in g_canMoveTiles:
    #                     # print('up,canmove', item)
    #                     if item[2][1] == '1':
    #                         flag_exit_move = 1
    #                         break
    #             elif event.key == K_LEFT  and g_keyLock == 1:
    #                 for item in g_canMoveTiles:
    #                     if item[2][0] == '1':
    #                         flag_exit_move = 1
    #                         break
    #             elif event.key == K_RIGHT  and g_keyLock == 1:
    #                 for item in g_canMoveTiles:
    #                     if item[2][2] == '1':
    #                         flag_exit_move = 1
    #                         break
    #             # print('item', item)
    #             setMoveState(item, flag_exit_move, event.key)
    #             if flag_exit_move == 1:
    #                 infoTextObj2 = infoFontObj.render(str(g_ClickCount)+"步", True, YELLOW, NAVYBLUE)
    #                 infoRectObj2 = infoTextObj2.get_rect()
    #                 infoRectObj2.center = (580, 150)
    #         # if item != "" and flag_exit_move == 1:  
    #         #     g_curTile = item
    #         #     g_orientation = event.key         
    #         #     g_keyLock = 0
    #         #     g_curRectCopy = item[0].copy()
    #         #     g_startMoveFlag = 1
       
            if event.key == 13: #重新开始
                pass
                
    #             StartGameSet(1)
    #             g_GAMESTART = 1
                # pygame.time.set_timer(COUNTTIMER, 3000) #启动游戏
                
    #             # infoTextObj2 = infoFontObj.render("0次", True, YELLOW, NAVYBLUE)
    #             # infoRectObj2 = infoTextObj2.get_rect()
    #             # infoRectObj2.center = (580, 130)
      
    # # textinput.update(events)
    if textinput.update(events):
        g_USERNAME = textinput.get_text()
        print(textinput.get_text())

                
    pygame.display.update()
    fpsClock.tick(FPS)