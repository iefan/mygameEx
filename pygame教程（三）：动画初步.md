### 前言

前面两章我们学习了利用`pygame`进行编程的基本框架，也学习了如何绘制基本的几何图形，这一章来学习如何使界面上的元素动起来。

如果学习过小海龟绘图的同学可能会发现，在小海龟中绘图我们是利用将小海龟设置为某种图形，然后在循环中将其位置不断改变即可。在`pygame`中，移动某种东西是利用`blit`函数进行的，该函数的功能是将某个`Surface`对象复制到指定的`Surface`对象上。

### 让小猫动起来

在学习`scratch`时，我们学习过如何使那只小猫在整个屏幕上跑来跑去，在这里，我们利用`pygame`也来完成同样的动作，看看有什么区别，下面先来看一下实现的动画效果：

（图）

代码如下：

```python
import pygame, sys
from pygame.locals import *

pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()
curSurface = pygame.display.set_mode((400, 340), 0, 32)
pygame.display.set_caption("Animation")

catImg = pygame.image.load("image/cat.png")
catImg = pygame.transform.smoothscale(catImg, (100,80))
catImg = pygame.transform.flip(catImg, 1, 0)

catx = 10
caty = 10
direction = 'right'
#设置颜色
WHITE = (255, 255, 255)
while True:
    curSurface.fill(WHITE)
    if direction == "right":
        catx += 5
        if catx == 280:
            direction = 'down'
    elif direction == 'down':
        caty += 5
        if caty == 220:
            direction = 'left'
    elif direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'up'
    elif direction == 'up':
        caty -= 5
        if caty == 5:
            direction = 'right'  
    curSurface.blit(catImg, (catx, caty))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS) 
```



这个程序比较简单，需要说明的几点如下：

1. FPS（Frame Per Second) 每秒帧率

   所有的动画必然牵扯到每秒帧率的问题，即每秒要播放多少帧画面，在`pygame`中，是利用`pygame.time.Clock`对象来实现的，为了创建它，直接调用即可：

   ```python
   fpsClock = pygame.time.Clock()
   ```

   然后在动画刷新结束，用这个对象的`tick`方法设定每秒帧率：

   ```python
   fpsClock.tick(FPS)
   ```

   如果不设定这个的话，动画效果是这样的：

   ![1](D:\思维导图\1.gif)

   从图上这种闪动频率来看，基本上没有任何意义，为了解决这个问题，我们为程序添加上帧率控制后的动画如下图所示：

   ![2](D:\思维导图\2.gif)

   这样子看起来就具备动画的节凑感了。

   当然我们也可以采用`time`包中的`time.sleep()`函数来实现，不过相对`pygame`自带的效果来说，后者视觉效果更好。

2. 图像加载、缩放

   加载图像用的是`pygame.image.load()`函数，要注意的是这里面要填写图片所在的路径及名称，绝对路径和相对路径都可以，这个函数也返回一个`Surface`对象，由于我们所用的图像本身比较大，所以在加载以后还要对其进行缩放处理，这需要用到`pygame.transform`包中的一个函数`smoothscale`，具体代码如下：

   ```python
   catImg = pygame.image.load("image/cat.png")  #加载
   catImg = pygame.transform.smoothscale(catImg, (100,80)) #缩放
   ```

   由于最开始的猫咪头像朝右，为了让其朝左，需要用到`pygame.transform`包中的`flip`函数：

   ```python
   catImg = pygame.transform.flip(catImg, 1, 0)
   ```

   这个翻转函数带三个参数，第一个即是要翻转的图像所在的`Surface`对象，第二、第三个分别是沿左右方向、上下方向翻转的布尔变量，在本例中要左右翻转，故将其第二个参数设置为1，第三个参数设置为0。

3. 图像移动

   图像移动要用到`blit`函数，代码如下：

   ```python
   curSurface.blit(catImg, (catx, caty))
   ```

   这个函数的功能即是在`curSurface`这个上面将`catImg`复制到`(catx, caty)`处，然后必须用以下代码填充背景：

   ```python
   curSurface.fill(WHITE)
   ```

   关于这个填充函数在上一章讲过，但在这个程序中，需要将其放入循环体内才可以随着图片的移动填充图片原所在的位置的颜色，如果将该填充背景的语句只放在`while`循环体之外，则动画会变成下图这样：
   
   ![3](D:\思维导图\3.gif)

### 动态完成翻转操作

上面讲述的如何使动画启动起来，如果模仿`scratch`中小猫左右移动并改变方向，则需要改变一下程序，如下代码所示：

```python
import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

curSurface = pygame.display.set_mode((400, 340), 0, 32)
pygame.display.set_caption("Animation")

catImg = pygame.image.load("image/cat.png")
catImg_right = pygame.transform.smoothscale(catImg, (100,80)) ##缩放
catImg_left = pygame.transform.flip(catImg_right, 1, 0) ## 水平翻转

catx = 10
caty = 100
direction = 'right'

#设置颜色
WHITE = (255, 255, 255)
while True:
    curSurface.fill(WHITE)
    if direction == "right":
        catx += 5
        if catx == 280:
            direction = 'left'
        curSurface.blit(catImg_right, (catx, caty))  
    elif direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'right'
        curSurface.blit(catImg_left, (catx, caty))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)
```

细心的同学会注意到上述代码循环体中针对不同的方向将移动不同的`Surface`对象，动画如下：

![4](D:\思维导图\4.gif)