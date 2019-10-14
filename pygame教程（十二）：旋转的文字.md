### 前言

前面几章我们研究了几个小游戏的开发流程，细心的同学们会觉察到这几个小程序的界面背景比较相似，而且游戏其中的逻辑性都比较强，相对于一些较大的游戏来说，这些小游戏缺乏一些优美的加载动画，一则是因为这些小程序本身并不像大的游戏程序需要加载相当多的数据，二则是因为我们要抛开这些枝节性的东西，更专注于程序本身，这样更便于同学们熟悉利用`pygame`来开发游戏的方法。

这一章，我们来研究一下利用`pygame`实现文字的旋转，下面一个动画是我们将要实现的内容，并围绕这个动画，我们要仔细探寻一下`pygame`在旋转文字或图形方面容易有哪些方便之处和不足之处。



### 文字旋转的第一种方法

在前面的章节中，我们已经学会了如何在界面上添加文字，而`pygame`本身有这样的特性，即其界面上的文字一旦被创建，大小则不能更改，在其官方文档上是这样描述的：`Once the font is created the size cannot be changed.`

于是为了改变文字的大小，我们直观的思路是要创建一个定时器，在定时器中按设定的时间间隔每次都创建一个字体对象，当然承着定时器的运行，字体大小的设定即可实现变化，在定时器中的设置为：

```python
def checkUserEvent():
    global g_Fontsize, g_fontObj, g_titleSurf2
    userEvents = pygame.event.get(TimerEvent1)
    if len(userEvents) == 0:
        return None
    if g_zoom_flag == 1:
        if g_Fontsize > 30 : 
            g_Fontsize -= 2            
    else:
        if g_Fontsize < 60 : 
            g_Fontsize += 2
    g_fontObj = pygame.font.SysFont("simhei", g_Fontsize)
    g_titleSurf2 = g_fontObj.render("抖动旋转", True, GREEN, YELLOW)
```

从以上代码可以看出，我们在定时器函数中不断改变三个全局变量，而其中的两个将在主函数的循环体中被`pygame`发送到界面上，代码如下：

```python
while True:
    curSurface.fill(NAVYBLUE)
    rotatedSurf2 = pygame.transform.rotate(g_titleSurf2, degrees2)
    rotatedRect2 = rotatedSurf2.get_rect()
    rotatedRect2.center = (WINDOWWIDTH//2, WINDOWHEIGHT // 2) 
    curSurface.blit(rotatedSurf2, rotatedRect2) 
    degrees2 += 3
```

在这里，我们用到了`pygame.transform.rotate`这个函数，它需要两个变量，第一个是要旋转的文字对象，第二个是度数，该函数执行完毕后将返回另一个字体对象，而返回的这个对象才是要被发送到界面上的，即第1个文字对象是本体，第2个文字对象才是真正的旋转体，后者必须依靠前者，这一点请同学们仔细体会。

它的运行界面如下图所示：



如果与上一张动图相比较的话，会发现这个旋转的效果中会出现抖动，而且其旋转与前者是不同的，下面图形说明了其旋转的方式：

![11](D:\思维导图\11-1571056000989.png)

要注意，若以该函数来旋转的话，文字对象本身是以它外面的长方形为界限，在整个长方形内部旋转的，而外部长方形只是长宽发生变化，其本身是不会旋转的。

### 文字旋转的第二种方法

从第一种旋转方法来看，这种抖动很多时候是我们不想看到的，对于大多数玩家而言，平滑的动画才能体现出一种愉悦的感觉，于是`pygame`提供了另一个函数，即`pygame.transform.rotozoom`，这个函数顾名思义即是旋转与缩放可同时进行，其后带三个参数，第一个还是文字或图形对象，第二个是要缩放的角度，第二个是绽放的比例系数。

如果采用这种方式，我们就不需要自定义定时器，即可在主循环体中直接变动角度及比例系数即可，代码如下:

```python
while True:
    curSurface.fill(NAVYBLUE)
    rotatedSurf1 = pygame.transform.rotozoom(titleSurf1, degrees1, g_scale)
    rotatedRect1 = rotatedSurf1.get_rect()
    rotatedRect1.center = (WINDOWWIDTH//2, WINDOWHEIGHT // 2) 
    curSurface.blit(rotatedSurf1, rotatedRect1) 
    if g_zoom_flag == 1:
        if g_scale > 0.2 : 
            g_scale -= 0.01
            degrees1 += 3
        else:
            g_zoom_flag = 0               
    else:
        if g_scale < 1.2 :
            g_scale += 0.01
            degrees1 -= 3
        else:
            g_zoom_flag = 1
```

上述代码的运行结果即为本章第一个动图所示，从其旋转效果来看，要比方法一好了许多，而代码也简洁了许多，为了进一步研究两者旋转的对比，现将两种旋转方式放置于同一个界面上，如下图所示：



从上面动图可以看出，这种旋转方式与第一种不同，它是将包裹着整个文本的长方形整体来旋转，这种旋转符合我们的直观感受。

### 小结

本章对文本对象的两种方式进行了仔细研究，同学们可以根据需要来选择要用的旋转方式，从第二种方法的实现来看，在既旋转又缩放的情况下，它较前一种简洁方便，只需要创建一次文字对象即可，这种方式在以后的游戏初始或结束动画中值得借鉴。