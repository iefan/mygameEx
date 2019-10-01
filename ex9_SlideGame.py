# -*- coding: utf-8 -*-
import pygame, sys, random
from pygame.locals import *
import os
import pygame_textinput

pos_x = 100
pos_y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (pos_x,pos_y) #设置窗口起始位置

pygame.init()

FPS = 500
fpsClock = pygame.time.Clock()
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
# g_BlankTileBlock = 15
g_LastBlankBlock = '' #当前空位
g_curTile = '' #当前移动的棋子
g_curRectCopy = '' #当前移动的棋子的位置保存
g_orientation = '' #当前移动的方向
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

infoHelpText = infoFontObj.render("按回车开始", True, YELLOW, NAVYBLUE)
infoHelpRect = infoHelpText.get_rect()
infoHelpRect.center = (570, 260)

nameText = infoFontObj.render("玩家：", True, WHITE, NAVYBLUE)
nameRect = nameText.get_rect()
nameRect.center = (570, 320)

# lstRankInfo = []
# lstRankNameAndTime = []
# flag_Start = 0

# g_startMoveFlag = 0
# g_keyLock = 1
# g_mouseLock = 1

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

# getRankInfo()

m = 4
n = 4
# lstTilesBlock = [0 for i in range(m*n)] 
#lstBlockFlag = [[0 for i in range(m)] for j in range(n)]
#lstBlockFlag_OVER = [[1 for i in range(m)] for j in range(n)]

def inverse_number(lstnumber):
    icount = 0
    for i in range(len(lstnumber)):
        for j in range(i):
            if lstnumber[i]<lstnumber[j]:
                icount += 1
    print('inverse_number:', icount)
    return icount

# print(inverse_number([2,1,3]))

def generatePos(flagRight = 0):
    global g_LastBlankBlock
    lstNum = list(range(1, 16))
    # random.shuffle(lstNum)
    # for ii in range(10):
    if flagRight == 1:
        random.shuffle(lstNum)
        while inverse_number(lstNum)%2 != 0:
            random.shuffle(lstNum)

    lstNum.append(16)
    for i in range(m*n):
        row = i // m
        col = i % m
        lstTilesBlock[i] = [pygame.Rect(70+col*(blockWidth+5),110+row*(blockWidth+5), blockWidth, blockWidth), lstNum[i], '0000']
        if lstTilesBlock[i][1] == 16:
            g_LastBlankBlock = lstTilesBlock[i]

# generatePos() #生成所有棋子的位置数据

#绘制背景
def drawBackGround():
    curSurface.fill(NAVYBLUE)
    for i in range(m*n):
        curblock = lstTilesBlock[i]
        if curblock[1] != 16:
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

def findCanMoveTiles():
    global g_LastBlankBlock
    lstCanMoveTile = []
    blankIndex = lstTilesBlock.index(g_LastBlankBlock)

    for i in range(m*n):
        lstTilesBlock[i][2] = '0000'
        # print(lstTilesBlock[i][1], end=',')
    # print()
    # print(blankIndex, '----------')
    row = blankIndex//m
    col = blankIndex % n
    # print('row-col:', (row, col), (row-1)>=0, (row-1)*m+col)
    left, top, right, bottom = -1, -1, -1, -1
    if (row-1)>=0:
        top = (row-1)*m+col
    if (row+1)<m:
        bottom = (row+1)*m+col
    if (col-1)>=0:
        left  =  row*m + (col-1)  
    if (col+1)<n:
        right = row*m + (col+1) 

    # print('************',[left, top, right, bottom])
    icount = -1
    for item in [right, bottom, left, top]:
        icount += 1
        if item!=-1:
            tmp = list(lstTilesBlock[item][2])
            tmp[icount] = '1'
            lstTilesBlock[item][2] = ''.join(tmp)
            # print(lstTilesBlock[item])
            lstCanMoveTile.append(lstTilesBlock[item])
    # print('-----', lstCanMoveTile)
    return lstCanMoveTile

def MoveTileToBlank():
    global g_startMoveFlag, g_keyLock, g_mouseLock, g_LastBlankBlock, g_curTile, g_orientation, g_canMoveTiles
    if g_curTile == '':
        return
    flag_moveEnd = 0
    if g_orientation == K_DOWN:
        if g_curTile[0].top < g_LastBlankBlock[0].top:
            g_curTile[0].top += 1
        else:
            g_LastBlankBlock[0].top = g_curRectCopy.top
            flag_moveEnd = 1
    elif g_orientation == K_UP:
        if g_curTile[0].top > g_LastBlankBlock[0].top:
            g_curTile[0].top -= 1
        else:
            g_LastBlankBlock[0].top = g_curRectCopy.top
            flag_moveEnd = 1
    elif g_orientation == K_LEFT:
        if g_curTile[0].left > g_LastBlankBlock[0].left:
            g_curTile[0].left -= 1
        else:
            g_LastBlankBlock[0].left = g_curRectCopy.left
            flag_moveEnd = 1
    elif g_orientation == K_RIGHT:
        if g_curTile[0].left < g_LastBlankBlock[0].left:
            g_curTile[0].left += 1
        else:
            g_LastBlankBlock[0].left = g_curRectCopy.left
            flag_moveEnd = 1

    if flag_moveEnd == 1:
        g_startMoveFlag = 0
        g_keyLock = 1 #解锁按键
        g_mouseLock = 1

        firstIndex = lstTilesBlock.index(g_curTile)
        secondIndex = lstTilesBlock.index(g_LastBlankBlock)
        lstTilesBlock[firstIndex],lstTilesBlock[secondIndex] = lstTilesBlock[secondIndex],lstTilesBlock[firstIndex]
        # print(lstTilesBlock)
        g_canMoveTiles = findCanMoveTiles()
        # print('canMoveTiles', g_canMoveTiles)

def setMoveState(item, flag_exit_move, orientation):
    global g_curTile, g_orientation, g_keyLock, g_mouseLock,g_curRectCopy, g_startMoveFlag
    if item != "" and flag_exit_move == 1:  
        g_curTile = item
        g_orientation = orientation         
        g_keyLock = 0
        g_mouseLock = 0
        g_curRectCopy = item[0].copy()
        g_startMoveFlag = 1
   
COUNTTIMER = pygame.USEREVENT #创建自定义事件，计时

g_GAMESTART, g_canMoveTiles = 0,0
lstTilesBlock = []

lstRankInfo = []
lstRankNameAndTime = []

g_startMoveFlag = 0
g_keyLock = 1
g_mouseLock = 1

def StartGameSet(flag_qishi=0): 
    global g_GAMESTART, g_canMoveTiles, lstTilesBlock, g_startMoveFlag, g_keyLock, g_mouseLock, lstRankInfo, lstRankNameAndTime
    lstRankInfo = []
    lstRankNameAndTime = []
    g_startMoveFlag = 0
    g_keyLock = 1
    g_mouseLock = 1

    getRankInfo()
    lstTilesBlock = [0 for i in range(m*n)] 
    generatePos(flag_qishi) #生成所有棋子的位置数据
    pygame.time.set_timer(COUNTTIMER, 0)
    g_GAMESTART = 0
    g_canMoveTiles = findCanMoveTiles()
    

StartGameSet()

while True:
    drawBackGround()
    if g_startMoveFlag:
        MoveTileToBlank()
                    
    # mouse_x,mouse_y = -1,-1
    
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            # mouse_x, mouse_y = event.pos
            # printTile(event.pos)
            if g_GAMESTART == 1:
                flag_exit_move = 0
                for item in lstTilesBlock:                
                    if item[0].collidepoint(event.pos) and (item in g_canMoveTiles) and g_mouseLock==1:
                        if item[2] == '1000':
                            flag_exit_move = 1
                            orientation = K_LEFT
                        elif item[2] == '0100':
                            flag_exit_move = 1
                            orientation = K_UP
                        elif item[2] == '0010':
                            flag_exit_move = 1
                            orientation = K_RIGHT
                        elif item[2] == '0001':
                            flag_exit_move = 1
                            orientation = K_DOWN
                        
                        setMoveState(item, flag_exit_move, orientation)
                    
            # print(mouse_x, mouse_y)
        
        elif event.type == COUNTTIMER:
            infoTextObj4 = infoFontObj.render(str(g_TotalSecond)+"秒", True, YELLOW, NAVYBLUE)
            g_TotalSecond += 1
            infoRectObj4 = infoTextObj4.get_rect()
            infoRectObj4.center = (580, 230)

            #程序结束
            overStr = ""
            overFinaly = ''.join('%s' % id for id in range(1,17))
            for item in lstTilesBlock:
                overStr += str(item[1])
            # print(overStr)
            # print(overFinaly)
            if overStr == overFinaly:
                g_GAMESTART = 0
                # print(lstBlockFlag)
                pygame.time.set_timer(COUNTTIMER, 0) #全部选完关闭计时

                lstRankNameAndTime.append([g_TotalSecond-1, g_USERNAME])
                lstRankNameAndTime.sort()
                rankInfoStr = ""
                tmplstrankname = []
                for  isecond, iname in lstRankNameAndTime:
                    if (iname not in tmplstrankname) and len(tmplstrankname)<=3:
                        tmplstrankname.append(iname)
                        rankInfoStr += iname + "," + str(isecond) + '秒\n'

                with open(r'rankSlide.dat', 'w', encoding='utf-8' ) as f:
                    f.write(rankInfoStr)

                lstRankNameAndTime = []
                getRankInfo() #调用最新排名
                    
            # print(g_TotalSecond)

        elif event.type == KEYUP:
            # print(event.key, chr(event.key)=='↑', pygame.key.get_mods())
            # g_canMoveTiles = findCanMoveTiles()
            # print('g_keyLock', g_keyLock)
            if g_GAMESTART == 1:
                item = ''
                flag_exit_move = 0
                if event.key == K_DOWN and g_keyLock == 1:
                    for item in g_canMoveTiles:
                        if item[2][3] == '1':
                            flag_exit_move = 1
                            break 
                elif event.key == K_UP and g_keyLock == 1:
                    for item in g_canMoveTiles:
                        # print('up,canmove', item)
                        if item[2][1] == '1':
                            flag_exit_move = 1
                            break
                elif event.key == K_LEFT  and g_keyLock == 1:
                    for item in g_canMoveTiles:
                        if item[2][0] == '1':
                            flag_exit_move = 1
                            break
                elif event.key == K_RIGHT  and g_keyLock == 1:
                    for item in g_canMoveTiles:
                        if item[2][2] == '1':
                            flag_exit_move = 1
                            break
                # print('item', item)
                setMoveState(item, flag_exit_move, event.key)
            # if item != "" and flag_exit_move == 1:  
            #     g_curTile = item
            #     g_orientation = event.key         
            #     g_keyLock = 0
            #     g_curRectCopy = item[0].copy()
            #     g_startMoveFlag = 1
       
            if event.key == 13: #重新开始
                StartGameSet(1)
                g_GAMESTART = 1
                pygame.time.set_timer(COUNTTIMER, 1000) #启动游戏
                
                infoTextObj2 = infoFontObj.render("0次", True, YELLOW, NAVYBLUE)
                infoRectObj2 = infoTextObj2.get_rect()
                infoRectObj2.center = (580, 130)
      
    # textinput.update(events)
    if textinput.update(events):
        g_USERNAME = textinput.get_text()
        print(textinput.get_text())

                
    pygame.display.update()
    fpsClock.tick(FPS)