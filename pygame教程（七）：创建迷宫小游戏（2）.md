### 前言

在上一章中，我们对“迷宫”小游戏的开发步骤进行了分析，并从图标选择、程序加载图标、绘制背景以及处理鼠标点击事件等方面进行了详细说明，本章将对游戏余下的部分进行详细解释。

### 匹配图标

我们已经学习了如何对鼠标点击事件进行图标的查找，由于游戏的规则是前后两次点击的图标相同才能一起展示，否则将绘制白色方块进行覆盖。这就要求对奇数次点击和偶数次点击进行记忆，具体代码如下：

```python
if g_ClickCount % 2 == 1: # 奇数点击，记录第一次
    first_ClickIcon = [lstIcon[indx_icon], curIcon]
else: # 偶数点击，记录第二次
    second_ClickIcon = [lstIcon[indx_icon], curIcon]
```

这一段代码在上一章讲述鼠标点击时有列举过，其作用是根据玩家点击的次数进行奇偶性判定，并将前后两次图标及其位置均保存。

由于我们只在偶数次点击时进行判断，所以在循环体内我们需要以下代码：

```python
if g_ClickCount%2==0 and second_ClickIcon[0] != first_ClickIcon[0]:
    pygame.time.wait(300)
    lastIcon = first_ClickIcon[1]
    thisIcon = second_ClickIcon[1]
    lstBlockFlag[lastIcon[0]][lastIcon[1]] = 0
    lstBlockFlag[thisIcon[0]][thisIcon[1]] = 0
```

### 记时功能

为了用到记时功能，我们需要创建自定义事件，以供定时器定时调用，在`pygame`中创建自定义事件非常简单，只需要一行代码即可，在创建完成后将其加入定时装置：

```python
DISPINFOTEXT = pygame.USEREVENT #创建自定义事件，计时
pygame.time.set_timer(DISPINFOTEXT, 1000)
```

`pygame.time.set_timer`函数是定时器函数，上述代码中，它的功能是将我们创建的自定义事件每隔1秒运行一次。

在创建定时器后，只需要在循环体内及时捕捉我们创建的事件即可：

```python
if event.type == DISPINFOTEXT:
    infoText = infoFont.render(str(g_TotalSecond)+"秒", True, YELLOW, NAVYBLUE)
    g_TotalSecond += 1
    infoRect = infoText.get_rect()
    infoRect.center = (580, 230)
```

上述代码的作用是每隔1秒更新一下显示信息，`g_TotalSecond`是一个全局变量，功能是当游戏开始的时候记时，当然在这个定时器检测事件代码中，我们需要判断游戏是否结束，这只需要将当前图标的显示状态与最终状态进行比较即可：

```python
#程序结束
if lstBlockFlag == lstBlockFlag_OVER:
	pygame.time.set_timer(DISPINFOTEXT, 0) #全部选完关闭计时
```

同学们应该能注意到，关闭一个事件只需要将`set_timer`的第二个参数设置为0即可。

### 排名功能

排名首先需要让游戏知道当前玩家是谁，这就牵扯到用户的输入问题，在`pygame`中，弹出普通的对话框让用户输入是一件非常困难的事情，有兴趣的同学可以研究一下`pygame-pgu`这个软件包，该软件包基于`pygame`开发，其输入模块是将`pygame`的所有键盘事件进行拦截，然后将字母显示于`surface`对象上，因此，用这种包来输入汉字目前是不太可能的。

在输入用户名这一方面，目前我采取的是一个小小的机巧，即利用`github`上的一个类`pygame_textinput`，该类相当于将刚才提到的包`pygame-pgu`中的输入模块单独列出，将相关的文件下载放入与本程序同一目录后，在程序中直接导入该类即可：

```python
import pygame_textinput
textinput = pygame_textinput.TextInput(initial_string=g_USERNAME, text_color=WHITE )
curSurface.blit(textinput.get_surface(), (540, 340))
```

为了获取该输入框中内容，需要在程序的主要循环体中拦截事件，普通的键盘输入时，其拦截函数返回`False`，只有当回车时，该函数才返回`True`，并可取得其中的输入内容：

```python
if textinput.update(events):
    g_USERNAME = textinput.get_text()
```

为了同步使用回车键，我们设定当玩家按下回车键时，游戏启动，同时记住用户的名字：

```python
if event.type == KEYUP:
    if event.key == 13: # 回车重新开始
        flag_Start = 1 # 游戏开始标志
        pygame.time.set_timer(DISPFIRST, 5000) # 玩家记忆时间
```

在游戏每次启动时，可读取以前玩家的排名：

```python
def getRankInfo():
    if os.path.exists('rank.dat'):
        with open('rank.dat', 'r') as f:
            icount = 0
            rankTmpText = infoFontObj.render("排名", True, YELLOW, NAVYBLUE)
            rankTmpRect = rankTmpText.get_rect()
            rankTmpRect.center = (570, 400+icount*30)
            lstRankInfo.append([rankTmpText, rankTmpRect])
            for irank in f.readlines():
                icount += 1
                irank = irank.strip()
                if len(irank) == 0:
                    break
                tmpname,tmpsecond = irank.split(',')
                lstRankNameAndTime.append([int(tmpsecond[:-1]), tmpname])

                rankTmpText = infoFontObj.render(irank, True, YELLOW, NAVYBLUE)
                rankTmpRect = rankTmpText.get_rect()
                rankTmpRect.center = (570, 400+icount*30)
                lstRankInfo.append([rankTmpText, rankTmpRect])
```

上述函数实现了读取玩家记录的功能，相应地，我们还要在每一局游戏结束时根据玩家的成绩，对前三名进行调整，当前程序设置为只记录前三名的成绩：

```python
#程序结束
if lstBlockFlag == lstBlockFlag_OVER:
    pygame.time.set_timer(DISPINFOTEXT, 0) #全部选完关闭计时
    lstRankNameAndTime.append([g_TotalSecond-1, g_USERNAME])
    lstRankNameAndTime.sort()
    rankInfoStr = ""
    for  isecond, iname in lstRankNameAndTime[:3]:
        rankInfoStr += iname + "," + str(isecond) + '秒\n'
        with open('rank.dat', 'w') as f:
            f.write(rankInfoStr)
```

### 写在本游戏开发结束之后

通过两章的学习，同学们应该对用`pygame`创建一个小游戏有了一个大致的了解，在创建的过程中，我们看到了使用`pygame`进行二维游戏创作具有相当的便捷性，同时也看到`pygame`的一些不足，当然这些不足可以在后续的学习中用更高级的处理方式进行解决。

说一些题外之话：开发一个游戏的本身在于让同学们了解游戏的基本原理，从本质上来说，所有的电子游戏都只是二进制的组合，但许多同学沉迷于游戏本身正在于游戏的关卡设计，这种虚拟的体验让很多人深陷其中不能自拔，这里面有太多心理方面的成因，但如果能了解游戏的开发原理，是否能让更多同学跳出游戏的本身来看待游戏，并能从游戏开发中学习到逻辑的应用、实际问题的处理呢？这种解决难题的乐趣是否能给予同学们更好更正面的激励呢？从我本人的经历来说，我的答案是肯定的，衷心希望更多的同学能多学习，少沉迷一些游戏吧！



