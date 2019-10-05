### 前言

这一章我们继续来学习游戏的设计，带孩子去科技馆，看到有一种叫做“汉诺塔”的小游戏，这个智力游戏应该很多同学听说过，它首先在三根柱子中的第一根上摆放大小不一的圆盘，然后要求玩家用最少的步数、最短的时间将第一根柱子上的圆盘通过第二根柱子移动到第三根柱子上。

我们来看一下游戏的最终动画：



### 游戏开发步骤

1. 绘制背景及三根柱子
2. 玩家通过先后点击两根柱子来表示移动
3. 计算机给出判断，是否可移动以及是否结束；

### 部分难点介绍

##### 保存三根柱子的状态

可为三根柱子分别设置三个数组，保存着各自的圆盘`rect`，而且从大小到排列，为方便起见，可将柱子的底盘也加入该数组，这样就始终可以用各数组的最后一个来进行比较：

```python
for i in range(3):
    tmpleft = dipanLeft+i*(dipanWidth+50)
    tmp_Dipan = pygame.Rect(tmpleft, dipanTop, dipanWidth, dipanHeight)
    g_PieRect.append(tmp_Dipan)
    zhuziLeft = tmpleft +(dipanWidth - zhuziWidth)//2
    tmp_Dipan = pygame.Rect(zhuziLeft, zhuziTop, zhuziWidth, zhuziHeight)
    g_PieRect.append(tmp_Dipan)
    
A_PieRect.append(g_PieRect[0])
B_PieRect.append(g_PieRect[2])
C_PieRect.append(g_PieRect[4])
for i in range(g_TotalPieNums):
    tmpleft = dipanLeft + (i+1)*lap
    pieWidth = dipanWidth - lap*2*(i+1)
    tmptop = dipanTop - (i+1)*(pieHeight+2)
    tmp_Dipan = pygame.Rect(tmpleft, tmptop, pieWidth, pieHeight)
    A_PieRect.append(tmp_Dipan)
```

##### 对玩家点击进行判断

因为玩家需要先后点击两根柱子才能移动，这就需要设计移动策略：

1. 当玩家第一次点击没有圆盘的柱子时，程序将不做反应

2. 当玩家点击两次有效柱子，并可使圆盘移动时，程序完成减少和添加动作

3. 当玩家点击两次有效柱子，但圆盘无法移动时，立刻清除标记状态

   

   代码如下：

```python
def calcClickFlag(pos):
    global g_FirstClick, g_SecondClick, g_ClickFlag, g_GAMEOVER
    if g_GAMEOVER:
        return
    # 当柱子所在的背景被点击的时候，改变相应的标记
    tmpPie = [A_PieRect, B_PieRect, C_PieRect]
    for i in range(3):
        if g_BGRECT[i].collidepoint(pos):
            if g_ClickFlag.count(1) == 0 and len(tmpPie[i])==1: #第一次点击时，底盘上没有圆盘
                break
            if g_ClickFlag[i] == 1:
                if i == g_FirstClick and g_ClickFlag.count(1)==1:#当只有1个被选中时，才能取消第1次点击的
                    g_FirstClick = -1
                    g_ClickFlag[i] = 0
                elif i == g_SecondClick:
                    g_SecondClick = -1
                    g_ClickFlag[i] = 0
            else:
                if g_ClickFlag.count(1) < 2: #如果连续点击三根柱子，则第三根不记录
                    g_ClickFlag[i] = 1
                    if g_FirstClick == -1:
                        g_FirstClick = i
                    elif g_SecondClick == -1:
                        g_SecondClick = i
    MovePie()
    isGameOver()
```

##### 移动圆盘

程序在玩家模式下只是简单将圆盘从一根柱子移动到另一根柱子，如果按向上箭头，即完成“飞盘”演示动画，移动圆盘的代码如下：

```python
def MovePie():
    global g_FirstClick, g_SecondClick, g_ClickFlag
    if g_FirstClick == -1 or g_SecondClick == -1:
        return
    # 每一个柱子数组都是从大到小排列
    tmpPie = [A_PieRect, B_PieRect, C_PieRect]
    firstPie = tmpPie[g_FirstClick][-1] #移动的圆盘
    secondPie = tmpPie[g_SecondClick][-1] #要移动到其上的圆盘（含底盘）

    if firstPie.width > secondPie.width: #大盘不能放在小盘上
        g_ClickFlag = [0,0,0]
        g_FirstClick, g_SecondClick = -1, -1
        return 
    firstPie.left = secondPie.left + (secondPie.width-firstPie.width)//2
    firstPie.top = secondPie.top - firstPie.height-2
    tmpPie[g_FirstClick].remove(firstPie)
    tmpPie[g_SecondClick].append(firstPie)
    g_ClickFlag = [0,0,0] #清除标记状态
    g_FirstClick, g_SecondClick = -1, -1
```



### 汉诺塔的解法

汉诺塔的解法其实只是一个递归循环，现将代码给出：

```python
import string
g_sn_arr = []
def gensnarr(arr, flagarr):
    [n1, n2, n3]=arr
    [a,b,c] = flagarr
    if n1==0 and n2==0:
        return
    else:
        gensnarr([n1-1, n2, n3], [a, c, b])
        g_sn_arr.append([a,c])
        gensnarr([n1-1, n2, n3], [b, a, c])
def hannuota(num=3):
    gensnarr([num,0,0], [1,2,3])
    indx = 0
    somepies = [string.ascii_uppercase[:num], '', '']
    print("原来状态：", somepies)
    for item in g_sn_arr:
        [i,j] = item
        i=i-1
        j=j-1
        somepies[j] = somepies[i][0]+somepies[j]
        somepies[i] = somepies[i][1:]
        indx += 1
        print("第%d步"%indx, item, somepies)
        
if __name__ == "__main__":
    hannuota(4)
```

控制台打印图如下所示：



### 将自动演示纳入游戏

可将上述代码纳入小游戏中，这样子更便于玩家研究“汉诺塔”的移动规律。自动演示只是将上述汉诺塔的解法生成的数据传递给移动函数，同时加入动画即可，代码如下：

```python
def autoMove():
    global g_sn_arr, g_FirstClick, g_SecondClick, g_AutoFlag
    g_AutoFlag = 1
    g_sn_arr = []
    hannuota_genarr([g_TotalPieNums,0,0], [0,1,2])
    g_FirstClick = g_sn_arr[0][0]
    g_SecondClick = g_sn_arr[0][1]
    MovePie()
```

### 小结

由上文可以看出，汉诺塔的解法是典型的递归法，但在制作游戏时其实用不到其解法，只需要忠实记录和按游戏规则规范玩家的动作即可，从两者对比也可以看出，解法与游戏的设计有联系，但侧重点是不同的，毕竟面向的方向不同，所以尽管同学们可能对解法不一定能熟悉，但是只要掌握了游戏的设计要领，同样可以制作出好玩的游戏。