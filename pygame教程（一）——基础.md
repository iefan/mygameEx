### 安装
关于`PyGame`的安装，如同`python`的第三方包一样，利用`pip`进行安装最为方便快捷：
```python
pip install pygame
```

在安装完成后，在`idle`中或是`ipython`等交互命令窗口利用以下代码可验证是成功：
```python
import pygame
```
如果上述代码没有报错，说明这个包已经成功安装，通常会打印出如下信息：
```python
pygame 1.9.6
Hello from the pygame community. https://www.pygame.org/contribute.html
```

### 动画基本框架
在介绍基本框架时，按照惯例，我们同样可用`hello world`来进行演示，代码如下：

```python
import pygame, sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('hello world!')

while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
```

上述代码一共分为五部分：

1.  第一部分：导入

   ```python
   import pygame, sys
   from pygame.locals import *
   ```

   上述导入的第二行代码是因为`pygame.locals`中含有一些常量，比如上述代码中的`QUIT`，以这种方式导入后，在使用时比较方便。

2.  第二部分：初始化

   ```python
   pygame.init()
   ```

   这一句代码是所有采用`pygame`包开发的游戏都必须包含的。

3.  第三部分：设定舞台大小及标题等元素

   ```python
   DISPLAYSURF = pygame.display.set_mode((400, 300))
   pygame.display.set_caption('hello world!')
   ```

   这里是对游戏主窗口一些元素的设定，要注意的是`set_mode`函数接收的是一个`tuple`数据类型，并不是两个孤立的数，这一数对指定了要创建窗口的宽和高。当然`set_caption`顾名思意就是设置窗口的标题了。

4.  第四部分：事件循环

   ```python
   while True:
       for event in pygame.event.get():
           ...
   ```

   这是游戏的主循环，如果有同学仔细研究了上次的`PySimpleGUI`教程的话，会发现这种处理方式与那个创建窗体后响应事件的方式非常类似，不同的是这里用`pygame.event.get()`获取用户对窗口的所有响应。这里要注意，由于用户在同一时间有可能会对窗体进行多种操作，所以`pygame.event.get()`将返回一个列表，该列表中每一个元素均为`pygame.event.Event`类型，当然，如果用户不曾操作窗体，该列表将为空。

5.  第五部分：在事件循环中对相应的事件进行处理

   ```python
   if event.type == QUIT:
       pygame.quit()
       sys.exit()
   ```

   在窗体检测到“退出”指令的时候，程序将首先退出`pygame`，这里的`pygame.quit()`是和`pygame.init()`完全相反的一种状态，即对其内部创建的东西进行销毁，但程序本身仍然运行，所以还需要调用`sys.exit()`才能退出整个程序，当然在整个主循环过程中，为了保证窗体能实时刷新，需要显式调用以下代码：
   
   ```python
   pygame.display.update()
   ```
   
   如果将窗体主循环以图形来表示的话，下面这个简图可以很好地说明整个程序是如何执行的：

![loop](D:\思维导图\loop.png)

### 坐标系统

对于创建动画来说，研究其坐标系统当然是必须的，下面以一个8X8的界面来说明其坐标方向的规定：

![cor](D:\思维导图\cor.png)

从上图可以看出，`pygame`的坐标系统与电脑屏幕的坐标系统正常，与小海龟`turtle`的坐标是不一样的，有兴趣的同学可以查看前面的教程。

### 颜色设定

在`pygame`中，颜色也是采用RGB方式来设定，从（0,0,0）到（255,255,255）一共有16,777,216种不同的颜色，下表简单列出一些常用的颜色，这些颜色可以用左边相应的字符串名称来表示：

|  颜色  |   名称    |   对应的RGB值   |
| :----: | :-------: | :-------------: |
| 湖绿色 |   Aqua    |  (0, 255, 255)  |
|  黑色  |   Black   |     (0,0,0)     |
| 紫红色 |  Fuchsia  |  (255,0, 255)   |
|  灰色  |   Gray    | (128, 128, 128) |
|  绿色  |   Green   |   ( 0, 128,0)   |
| 绿黄色 |   Lime    |   ( 0, 255,0)   |
| 紫褐色 |  Maroon   |    (128,0,0)    |
| 海军蓝 | Navy Blue |   ( 0,0, 128)   |
| 橄榄绿 |   Olive   |  (128, 128,0)   |
|  紫色  |  Purple   |  (128,0, 128)   |
|  红色  |    Red    |    (255,0,0)    |
|  银色  |  Silver   | (192, 192, 192) |
| 蓝绿色 |   Teal    | ( 0, 128, 128)  |
|  白色  |   White   | (255, 255, 255) |
|  黄色  |  Yellow   |  (255, 255,0)   |
|  蓝色  |   Blue    |   ( 0,0, 255)   |

在颜色设定中，还可以设置透明度，此时颜色与透明度组成四元数组，用`tuple`表示为：`（R, G, B, T）`，透明度`T`也是从0到255；为了用透明度来绘制界面，在代码中必须用`convert_alpha()`创建一个`Surface`对象，比如：

```
anotherSurface = DISPLAYSURF.convert_alpha()
```

然后再用`blit`或`pygame.image.load()`进行绘制时即可出现透明效果，关于这部分在后续章节将会详细介绍。

创建一种颜色对象有两种方式，以下代码展示了这两种情况：

```python
>>> import pygame                                                           
>>> mycolor = pygame.Color(255,128,0)                                       
>>> mycolor == (255,128,0,255)                                              
True
>>> 
```

### 创建区域

创建一个绘图区域，同样有两种方式：

第一种是以`(X, Y, Width, Height)` 来创建，其中 X和Y分别是所创建区域的左上角顶点的横纵坐标，按`pygame`的坐标系统，这两都均为正值，后两项分别规定了所创建区域的宽和高。

第二种是用`pygame.Rect`来创建，以下代码演示了两者相同：

```python
>>>  import pygame 
>>>  myrect = (10, 20, 100,300)                                              
>>>  myrect2 = pygame.Rect(10, 20, 100, 300)  
>>>  myrect == myrect2                                                       
True
>>>  
```

对于创建的区域`rect`，其有以下属性，列表以备查询：

| Attribute Name     | Description                     |
| :----------------- | ------------------------------- |
| myRect.left        | 区域左边横坐标，整数            |
| myRect.right       | 区域右边横坐标，整数            |
| myRect.top         | 区域上边纵坐标，整数            |
| myRect.bottom      | 区域下边纵坐标，整数            |
| myRect.centerx     | 区域中心横坐标，整数            |
| myRect.centery     | 区域中心纵坐标，整数            |
| myRect.width       | 区域宽度，整数                  |
| myRect.height      | 区域高度，整数                  |
| myRect.size        | 宽高二元数组，(width, height)   |
| myRect.topleft     | 左上顶点坐标: (left, top)       |
| myRect.topright    | 右上顶点坐标: (right, top)      |
| myRect.bottomleft  | 左下顶点坐标: (left, bottom)    |
| myRect.bottomright | 右下顶点坐标: (right, bottom)   |
| myRect.midleft     | 左边中点坐标: (left, centery)   |
| myRect.midright    | 右边中点坐标: (right, centery)  |
| myRect.midtop      | 上边中点坐标: (centerx, top)    |
| myRect.midbottom   | 下边中点坐标: (centerx, bottom) |

