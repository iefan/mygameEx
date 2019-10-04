### 前言

上几章我们学习了两个小游戏的制作，同学们应该发现这些小游戏都离不开鼠标或键盘的输入，在这一章，我们继续来制作小游戏，但这个小游戏要稍难一点，很挑战玩家的智力推理能力，与前两个小游戏不一样的是，这个小游戏的制作相对而言不会那有那么多的开关变量来控制其状态，只需要如实记录玩家的策略即可，说了这么多，同学们一定想知道这个小游戏是什么了吧？对了，是著名的“猜数字游戏”，下面来看一下制作完成后的效果图吧：



### 游戏说明

这个“猜数字”游戏是从0~9这10个数字中随机选取4个数字，然后给玩家最多7次机会猜测，对每次玩家猜的结果用“几A几B”来表示，A表示是的猜的数字正确位置也正确，而B则表示猜的数字正确但位置不正确。

例如：计算机随机从0~9中选定4个数字：4，6，7，2；玩家的某次猜测为5，6，2，8，那么计算机将给出判断：1A1B。

玩家根据计算机的提示，不断修正自己的猜测，从理论上来说，猜出这四个数字，最多只需要7次机会即可。

### 游戏开发步骤

1. 从0~9十个数字中随机选取4个；
2. 玩家输入自己的猜测；
3. 计算机给出判断，并结合玩家的输入次数来确定结束与否；
4. 对成功的结果进行时间记录，重新开启新一局

### 部分难点介绍

##### 判断用户点击

可将十个数字方块放置在界面上供用户输入，保存这十个方块的`rect`，在鼠标点击时判断哪个数字被点击，同时记录该数字，代码如下：

```python
def numberClick(pos):
    global g_GAMEOVER
    if g_GAMEOVER:
        return
    if g_NumberRect[-1][0].collidepoint(pos) and len(g_UserGuessNumber)==4: #确认
        judgeGuessIsRight(g_UserGuessNumber.copy()) ## 判断是否正确
        g_UserGuessNumber.clear()    
    for item in g_NumberRect[:-1]:
        if item[0].collidepoint(pos):
            if item[1] in g_UserGuessNumber:
                g_UserGuessNumber.remove(item[1]) # 两次点击可取消当前选定的数字
            else:
                if len(g_UserGuessNumber)<4:
                    g_UserGuessNumber.append(item[1])    
            break     
```

##### 判断游戏是否结束

可将事先生成的随机数保存起来，也将玩家的输入数据存储，在每次玩家点击确认提交时进行判断比对：

```python
def judgeGuessIsRight(userguessname):
    global g_GAMEOVER
    if g_GAMEOVER:
        return
    A_count = 0
    B_count = 0
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
```

以上代码对玩家的输入进行判断，并标明正误情况，以便于玩家进行下一步判断。

### 小结

这个“猜数字”游戏的小程序很容易制作，同学们可以练习一下，甚至可将平常想到的小游戏都用`pygame`来完成一下，一则可以熟悉`pygame`在平面游戏制作方面的优缺点，二则可以在制作这些小游戏时对其逻辑的分析更深入。