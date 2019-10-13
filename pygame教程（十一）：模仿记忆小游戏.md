### 前言

在前面一些章节中，我们学习了`pygame`制作平面游戏的一些方法，上一章中，我们利用`pygame`制作了一部热门电影的片头字幕动画，这一章，我们继续来利用`pygame`实战另一个古老的小游戏。

这个小游戏英文名称叫`Simon`，翻译过来，有叫“西蒙游戏”的，有叫“模拟记忆游戏”的等，它是一款经典的重复游戏，玩家要做的就是不停地将电脑闪过的图形顺序重复，电脑会根据玩家的熟练程度来加大随机序列的长度。这款游戏主要训练的是玩家的瞬时记忆能力。

来看一下我们利用`pygame`制作的游戏动图：



### 游戏设计思路

这个游戏看起来思路相当简单，但实际上在完成时，还是有一定的难度。下面先列举一下游戏设计步骤：

1. 绘制界面，并随机生成序列
2. 根据随机序列改变各个方块的亮度
3. 在计算机闪现结束后，等待玩家鼠标点击
4. 记录玩家点击顺序并开启倒计时模式
5. 在玩家完成后或倒计时完成时结束这一轮
6. 根据结果判断是否结束游戏或进入下一轮



### 游戏设计难点

**生成随机序列及明暗显示**是这个程序最主要的难点。

`pygame`的动画绘制方式是在主循环中不停地刷新，我们能做的就是在外部改变相应的变量，因为游戏中有四个着色方块，所以在同一时刻只能有一个方块变亮，而在其变亮一定时间后，需要再将其变暗，本程序采用的是一个数组来记录各个着色块的亮暗，该数组默认设置为`[0,0,0,0]`，当其中一个色块要这亮时，将其中一个位置改变为1，生成随机序列的函数代码如下：

```python
def genRandlist(n=1):
    global g_CurSn
    g_CurSn = ''
    lstrandslash = []
    for i in range(n):
        tmp = [0,0,0,0]
        tmpint = random.randint(0,3)
        tmp[tmpint] = 1
        g_CurSn += str(pow(2, tmpint)) #将每一次显示转换为对应的十进制
        lstrandslash.append(tmp.copy())
        lstrandslash.append([0,0,0,0])
    return lstrandslash.copy(), lstbeepFlag.copy()
```

而对应在主循环体中显示亮度的代码如下：

```python
lstColor = [YELLOW_D, RED_D, GREEN_D, WHITE_D]
lstColor2 = [YELLOW, RED, GREEN, WHITE]
for i in range(4):
    if slash == 0:
        pygame.draw.rect(curSurface, lstColor[i], g_lstBlockRect[i])
    elif slash == 1 or slash == 2: #计算机显示或玩家点击时均要设置亮度
        if g_lstslash[i]==1:
            pygame.draw.rect(curSurface, lstColor2[i], g_lstBlockRect[i])
        else:
            pygame.draw.rect(curSurface, lstColor[i], g_lstBlockRect[i])
```

**定时器设定**

是本程序设计的另一个难点，当游戏开始运行时，要启动第一个定时器（将其称为定时器1），它的功能是生成每一轮的随机序列，这个随机序列是一个二维数组，其每一个元素代表色块要显示的状态，它每隔一段时间将这个随机序列的指针往后移动一位，以便于改变显示状态，在整个随机序列显示完成后，一方面它将变量控制权交给玩家的鼠标点击事件，一方面它启动倒计时定时器（将其称为定时器2），定时器2的功能是监督玩家的回忆时间，一旦玩家在规定时间内没有完成序列重现，将判断本局游戏因超时作答而失败。

玩家点击每一个色块后，将立刻启动第三个显示定时器（称其为定时器3），定时器3的功能是一次性闪现玩家的点击色块，在一次调用结束时，自动关闭其本身，等待下一次玩家点击时再来启动。

三个自定义定时器的代码如下：

```python
		if event.type == GAMETIMER: #定时器2
            g_lstslash = [0,0,0,0]
            if g_GAMESTART == 1:
                g_GAMESTART = 0
                g_COUNT_SUCCESS = 0
                pygame.time.set_timer(COUNTTIMER, 0)
                pygame.time.set_timer(TIMERUSERDISP, 0)
                pygame.time.set_timer(GAMETIMER, 0)
                successText = infoFontObj.render("超时挑战失败！", True, RED, NAVYBLUE)
                getRankInfo('write')
            pygame.time.set_timer(GAMETIMER, 0) #结束当前

        elif event.type == TIMERUSERDISP: #定时器3
            g_lstslash = [0,0,0,0]
            g_Slash == 2
            if len(g_CurSn) == len(g_CurSn_user):
                if g_CurSn == g_CurSn_user:
                    g_COUNT_SUCCESS += 1
                    io2 = if2.render(str(g_COUNT_SUCCESS)+"次", True, YELLOW, NAVYBLUE)
                    successText = infoFontObj.render("恭喜，成功！", True, YELLOW, NAVYBLUE)
                    pygame.time.set_timer(COUNTTIMER, 300)
                    pygame.time.set_timer(GAMETIMER, 0)
                else:
                    g_GAMESTART = 0
                    g_COUNT_SUCCESS = 0
                    pygame.time.set_timer(COUNTTIMER, 0)
                    pygame.time.set_timer(TIMERUSERDISP, 0)
                    pygame.time.set_timer(GAMETIMER, 0)
                    successText = infoFontObj.render("遗憾，失败！", True, RED, NAVYBLUE)
                    getRankInfo('write')
                g_Slash = 1
                g_CurSn_user = ''
            pygame.time.set_timer(TIMERUSERDISP, 0)

        elif event.type == MOUSEBUTTONUP: #玩家鼠标点击
            if g_GAMESTART == 1 and g_Slash == 2: #当显示结束才可以点击
                g_lstslash = [0,0,0,0]
                for i in range(4):                
                    if g_lstBlockRect[i].collidepoint(event.pos):
                        g_CurSn_user += str(pow(2,i))
                        g_lstslash[i] = 1
                        pygame.time.set_timer(TIMERUSERDISP, 300)
                        g_Slash == 1
                print(g_CurSn, g_CurSn_user, g_CurSn==g_CurSn_user, g_lstslash)
        
        elif event.type == COUNTTIMER: #定时器1
            if g_slashcount == 0 and g_Slash == 1:
                gg_lstslashAll = genRandlist(g_GAME_CONTROL_LIST[g_COUNT_SUCCESS]) #新一轮游戏
                g_Slash = 1
                g_lstslash = [0,0,0,0]

            if g_slashcount<len(gg_lstslashAll) and g_Slash==1:
                g_lstslash = gg_lstslashAll[g_slashcount]
                g_slashcount += 1
            else:
                g_Slash = 2 #开始玩家点击
                g_slashcount = 0
                g_lstslash = [0,0,0,0]
                pygame.time.set_timer(COUNTTIMER, 0)
                pygame.time.set_timer(GAMETIMER, len(gg_lstslashAll)*800) #启动游戏倒计时
```

**关于游戏结束的判断**

因只有4个色块，每个色块是明暗两种颜色，所以可将其按二进制数来计算，转成对应的十进制为即为1、2、4、8，所以在每一轮游戏开始时，生成的序列可记作`'128414...'`样式，然后在用户点击中也实时记录，当两者长度相同时，即开始判断正误，若正确，则将控制权交还定时器1，若错误，直接将三个定时器均关闭，结束游戏；同时在定时器2中也实时监控着玩家的用时，若超时，则同样结束游戏。

### 小结

从代码量上看，本小游戏代码并不多，但因涉及到三个定时器，所以其间的开关控制变量相对来说逻辑就比较复杂，只有思路清晰，认真调试，才能确保程序的成功运行。