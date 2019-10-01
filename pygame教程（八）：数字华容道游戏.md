### 前言

前两章我们学习了游戏的初步实战，利用所学的知识编写了一个记忆迷宫小游戏，较综合地练习了用`pygame`开发游戏的流程及相关的知识，这一章，我们继续进入游戏实战，利用所学的知识开发一个“数字华容道”小游戏。

### 数字华容道简介

喜欢玩智力游戏的同学们应该会熟悉这个玩法，以通常的4阶为例，即在4X4的方格中填写1~15共15个数字棋子，空出一个方格，通过不断移动棋子，将所有数字按顺序从小到大排列完毕，下面动画是我们游戏完成的最终形态：



如果有看过《最强大脑》的同学，应该还记得在有一季选拔赛中，就有用《数字华容道》这道题目来选拔选手。在本章，我们将来学习如何用`pygame`来开发这一款小游戏。

### 游戏思路

作为游戏开发者，自然不只是要研究如何去解答题目，而是要对游戏各种意外进行分析并编写相应代码来规范用户输入行为，下面列举一下这个游戏的开发步骤：

1. 绘制背景及初始布局。
2. 根据数字序列的逆序数奇偶性来生成新题目。
3. 处理键盘四个方向键的响应。
4. 处理鼠标点击响应。
5. 计时、计步并进行结束判断。
6. 保存玩家成绩。

### 疑难问题处理

#### 计算数字序列的奇偶性

需要注意的是：并不是任意生成的随机数列均存在答案，由于初始空位的存在位置及生成数列的逆序数奇偶性，需要对这些情况进行一一计算，首先我们固定初始位置于位4X4方格的右下角，在这种情况下，只需要保证1~15这十五个数随机生成序列的逆序数为偶数即可，计算逆序数的函数如下：

```python
def inverse_number(lstnumber):
    icount = 0
    for i in range(len(lstnumber)):
        for j in range(i):
            if lstnumber[i]<lstnumber[j]:
                icount += 1
    return icount
```

#### 构建数字棋子节点

由于每个数字棋子需要记录其位置、显示其上数字以及记录其将移动的方向，所以可将每一个棋子元素设计为如下形式：

numberChess = [位置数据，数字，可移动标记]

因为每个数字棋子最多只有四个方向可移动，且其每一次只可能有一个移动方向，所以这里将可移动标记设为'0000'字符串，分别代表“左上右下”位置，当每个位置上变为1时，即代表相关的位置可移动，比如'0100'即代表该数字棋子可向上移动，假如此时玩家按下“向上”键时，该棋子即向上移动一格。

代码如下:

```python
def generatePos(flagRight = 0):
    global g_LastBlankBlock
    lstNum = list(range(1, 16))
    if flagRight == 1:
        random.shuffle(lstNum)
        # 根据序列的奇偶性生成题目
        while inverse_number(lstNum)%2 != 0:
            random.shuffle(lstNum)
    lstNum.append(16)
    for i in range(m*n):
        row = i // m
        col = i % m
        lstTilesBlock[i] = [pygame.Rect(70+col*(W+5),110+row*(W+5), W, W), lstNum[i], '0000']
        if lstTilesBlock[i][1] == 16:
            g_LastBlankBlock = lstTilesBlock[i]
```

以上代码完成了题目的生成，该函数所带参数是区分初始状态和解题状态。

#### 查找可移动的数字棋子

当我们固定了一个空位后，需要即时计算出该空位四周的数字棋子，并将其可移动方向标记下来，这个应该不困难，根据行、列加减一后即可判断，代码如下：

```python
def findCanMoveTiles():
    global g_LastBlankBlock
    lstCanMoveTile = []
    blankIndex = lstTilesBlock.index(g_LastBlankBlock)
    for i in range(m*n):
        lstTilesBlock[i][2] = '0000'
    row = blankIndex//m
    col = blankIndex % n
    left, top, right, bottom = -1, -1, -1, -1
    if (row-1)>=0:        top = (row-1)*m+col
    if (row+1)<m:        bottom = (row+1)*m+col
    if (col-1)>=0:        left  =  row*m + (col-1)  
    if (col+1)<n:        right = row*m + (col+1) 
    icount = -1
    for item in [right, bottom, left, top]:## 注意与左上右下正好相反，改变标记
        icount += 1
        if item!=-1:
            tmp = list(lstTilesBlock[item][2])
            tmp[icount] = '1'
            lstTilesBlock[item][2] = ''.join(tmp)
            lstCanMoveTile.append(lstTilesBlock[item])
    return lstCanMoveTile
```

由于我们设置的标记是字符串，每次变更需要对其进行修改，这段代码还可以优化。

#### 移动棋子到空位并交换

当玩家按下方向键后，需要判断当前是否有数字棋子可供移动，若有，则将可移动棋子与空位交换，此时用动画处理，代码如下：

```python
def MoveTileToBlank():
    global g_startMoveFlag,g_ClickCount, g_keyLock, g_mouseLock, g_LastBlankBlock, g_curTile, g_orientation, g_canMoveTiles
    if g_curTile == '':        return
    flag_moveEnd = 0
    if g_orientation == K_DOWN:
        if g_curTile[0].top < g_LastBlankBlock[0].top:
            g_curTile[0].top += 1 #动画处理
        else:
            g_LastBlankBlock[0].top = g_curRectCopy.top
            flag_moveEnd = 1
   elif g_orientation == K_UP:
## .........................其它类似代码................................
    if flag_moveEnd == 1: #交换
        f1 = lstTilesBlock.index(g_curTile)
        f2 = lstTilesBlock.index(g_LastBlankBlock)
        lstTilesBlock[f1],lstTilesBlock[f2] = lstTilesBlock[f2],lstTilesBlock[f1]
        g_canMoveTiles = findCanMoveTiles()
```

需要注意的是，对于列表而言，交换其两个元素，需要直接引用列表，这样才能交换列表中两元素的次序。

#### 处理键盘和鼠标事件

处理方向键比较容易，这一点在上一次游戏中我们有专门讲述，这里只列举一段代码，有练习过的同学很容易看明白：

```python
if event.key == K_DOWN and g_keyLock == 1:
    for item in g_canMoveTiles:
        if item[2][3] == '1':
            flag_exit_move = 1
            break 
        elif event.key == K_UP and g_keyLock == 1:
            # ......其他代码......
setMoveState(item, flag_exit_move, event.key) #调用动画的一些参数设置
```

对于鼠标的处理，上一章中，我们直接获取鼠标的位置，自己写了代码来检测当前鼠标是否在相关方块上点击，这一次我们采取另一种更有效的方法，即直接可用`pygame.Rect`的`collidepoint`方法，如果鼠标在该区域点击，该方法返回`True`，否则返回`False`。代码如下：

```python
for item in lstTilesBlock:                
    if item[0].collidepoint(event.pos) and (item in g_canMoveTiles) and g_mouseLock==1:
        if item[2] == '1000':
            flag_exit_move = 1
            orientation = K_LEFT
        elif item[2] == '0100':
            # ......其他代码......
 setMoveState(item, flag_exit_move, orientation) #调用动画的一些参数设置
```

细心的同学应该注意到键盘和鼠标的响应我们调用的是同一个函数，因为这部分功能是相同的，所以可将其单独提取出来成一个函数，这将起到代码重用的作用。

### 小结

在本章，我们讲述了如何开发一个“数字华容道”的基本步骤，其中有部分功能与上一个记忆迷宫的游戏类似，本章只对部分关键内容进行了讲解，当然在游戏开发过程中还有不少的开关变量需要设置，这一部分内容细琐繁杂，不太适合文字表述，有愿意进一步了解的可在公众号内留言。